import asyncio

import pytest
from fastapi import HTTPException, Request

from app.api.decorators import authn
from app.data.csrf import generate_csrf_token
from app.data.entities import Session
from app.data.interfaces import IAuthClient

CSRF_SECRET = "test-secret"
VALID_SESSION = Session(id="session-1", identity_id="user-1")
VALID_CSRF_TOKEN = generate_csrf_token(VALID_SESSION.id, CSRF_SECRET)


class FakeAuthClient(IAuthClient):

    def __init__(
        self,
        valid_cookie: str | None = "valid-cookie",
        valid_token: str | None = "valid-token",
    ):
        self._valid_cookie = valid_cookie
        self._valid_token = valid_token

    def whoami(self, cookie=None, token=None) -> Session | None:
        if cookie is not None and cookie == self._valid_cookie:
            return VALID_SESSION
        if token is not None and token == self._valid_token:
            return VALID_SESSION
        return None

    async def awhoami(self, cookie=None, token=None) -> Session | None:
        return self.whoami(cookie=cookie, token=token)


def _make_request(
    cookie: str | None = None,
    session_token: str | None = None,
    csrf_token: str | None = None,
) -> Request:
    headers = []
    if cookie is not None:
        headers.append((b"cookie", f"ory_kratos_session={cookie}".encode()))
    if session_token is not None:
        headers.append((b"x-session-token", session_token.encode()))
    if csrf_token is not None:
        headers.append((b"x-csrf-token", csrf_token.encode()))
    scope = {
        "type": "http",
        "headers": headers,
        "method": "GET",
        "path": "/",
    }
    return Request(scope)


@pytest.fixture(autouse=True)
def csrf_secret(monkeypatch):
    monkeypatch.setattr("app.api.decorators.settings.csrf_secret", CSRF_SECRET)


def _call(**kwargs):
    return asyncio.run(authn.__wrapped__(**kwargs))


def test_rejects_missing_credentials():
    with pytest.raises(HTTPException) as exc_info:
        _call(request=_make_request(), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 401


def test_rejects_invalid_cookie():
    with pytest.raises(HTTPException) as exc_info:
        _call(request=_make_request(cookie="wrong"), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 401


def test_rejects_valid_cookie_without_csrf():
    with pytest.raises(HTTPException) as exc_info:
        _call(request=_make_request(cookie="valid-cookie"), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 403


def test_rejects_valid_cookie_with_wrong_csrf():
    with pytest.raises(HTTPException) as exc_info:
        _call(
            request=_make_request(cookie="valid-cookie", csrf_token="wrong-token"),
            auth_client=FakeAuthClient(),
        )
    assert exc_info.value.status_code == 403


def test_rejects_valid_cookie_with_csrf_token_bound_to_other_session():
    other_session_csrf_token = generate_csrf_token("session-2", CSRF_SECRET)
    with pytest.raises(HTTPException) as exc_info:
        _call(
            request=_make_request(cookie="valid-cookie", csrf_token=other_session_csrf_token),
            auth_client=FakeAuthClient(),
        )
    assert exc_info.value.status_code == 403


def test_passes_valid_cookie_with_valid_csrf():
    session = _call(
        request=_make_request(cookie="valid-cookie", csrf_token=VALID_CSRF_TOKEN),
        auth_client=FakeAuthClient(),
    )
    assert session == VALID_SESSION


def test_rejects_invalid_session_token():
    with pytest.raises(HTTPException) as exc_info:
        _call(request=_make_request(session_token="wrong"), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 401


def test_passes_valid_session_token_without_csrf():
    session = _call(
        request=_make_request(session_token="valid-token"), auth_client=FakeAuthClient()
    )
    assert session == VALID_SESSION
