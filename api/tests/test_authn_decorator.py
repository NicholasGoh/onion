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


def test_sync_route_rejects_missing_credentials():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    with pytest.raises(HTTPException) as exc_info:
        route(request=_make_request(), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 401


def test_sync_route_rejects_invalid_cookie():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    with pytest.raises(HTTPException) as exc_info:
        route(request=_make_request(cookie="wrong"), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 401


def test_sync_route_rejects_valid_cookie_without_csrf():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    with pytest.raises(HTTPException) as exc_info:
        route(request=_make_request(cookie="valid-cookie"), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 403


def test_sync_route_rejects_valid_cookie_with_wrong_csrf():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    with pytest.raises(HTTPException) as exc_info:
        route(
            request=_make_request(cookie="valid-cookie", csrf_token="wrong-token"),
            auth_client=FakeAuthClient(),
        )
    assert exc_info.value.status_code == 403


def test_sync_route_passes_valid_cookie_with_valid_csrf():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    result = route(
        request=_make_request(cookie="valid-cookie", csrf_token=VALID_CSRF_TOKEN),
        auth_client=FakeAuthClient(),
    )
    assert result == "ok"


def test_sync_route_rejects_invalid_session_token():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    with pytest.raises(HTTPException) as exc_info:
        route(request=_make_request(session_token="wrong"), auth_client=FakeAuthClient())
    assert exc_info.value.status_code == 401


def test_sync_route_passes_valid_session_token_without_csrf():
    @authn
    def route(request: Request, auth_client: IAuthClient):
        return "ok"

    result = route(
        request=_make_request(session_token="valid-token"), auth_client=FakeAuthClient()
    )
    assert result == "ok"


def test_async_route_rejects_missing_credentials():
    @authn
    async def route(request: Request, auth_client: IAuthClient):
        return "ok"

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(route(request=_make_request(), auth_client=FakeAuthClient()))
    assert exc_info.value.status_code == 401


def test_async_route_passes_valid_session_token():
    @authn
    async def route(request: Request, auth_client: IAuthClient):
        return "ok"

    result = asyncio.run(
        route(
            request=_make_request(session_token="valid-token"),
            auth_client=FakeAuthClient(),
        )
    )
    assert result == "ok"


def test_async_route_passes_valid_cookie_with_valid_csrf():
    @authn
    async def route(request: Request, auth_client: IAuthClient):
        return "ok"

    result = asyncio.run(
        route(
            request=_make_request(cookie="valid-cookie", csrf_token=VALID_CSRF_TOKEN),
            auth_client=FakeAuthClient(),
        )
    )
    assert result == "ok"
