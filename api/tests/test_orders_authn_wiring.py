from unittest.mock import AsyncMock, MagicMock

from app.data.config import settings
from app.data.csrf import generate_csrf_token
from app.data.entities import Session
from app.main import container

VALID_SESSION = Session(id="session-1", identity_id="user-1")


def test_quote_route_rejects_missing_credentials(authn_client):
    mock_client = MagicMock(awhoami=AsyncMock(return_value=None))
    with container.kratos_client.override(mock_client):
        resp = authn_client.post("/orders/quote", json={"itemIds": [1], "quantity": {"1": 2}})
    assert resp.status_code == 401


def test_quote_route_rejects_valid_cookie_without_csrf(authn_client):
    mock_client = MagicMock(awhoami=AsyncMock(return_value=VALID_SESSION))
    authn_client.cookies.set("ory_kratos_session", "any-cookie")
    with container.kratos_client.override(mock_client):
        resp = authn_client.post("/orders/quote", json={"itemIds": [1], "quantity": {"1": 2}})
    assert resp.status_code == 403


def test_quote_route_accepts_valid_cookie_with_valid_csrf(authn_client):
    mock_client = MagicMock(awhoami=AsyncMock(return_value=VALID_SESSION))
    authn_client.cookies.set("ory_kratos_session", "any-cookie")
    csrf_token = generate_csrf_token(VALID_SESSION.id, settings.csrf_secret)
    with container.kratos_client.override(mock_client):
        resp = authn_client.post(
            "/orders/quote",
            json={"itemIds": [1], "quantity": {"1": 2}},
            headers={"X-CSRF-Token": csrf_token},
        )
    assert resp.status_code == 200
    mock_client.awhoami.assert_called_once()


def test_quote_route_accepts_valid_session_token(authn_client):
    mock_client = MagicMock(awhoami=AsyncMock(return_value=VALID_SESSION))
    with container.kratos_client.override(mock_client):
        resp = authn_client.post(
            "/orders/quote",
            json={"itemIds": [1], "quantity": {"1": 2}},
            headers={"X-Session-Token": "any-token"},
        )
    assert resp.status_code == 200
    mock_client.awhoami.assert_called_once()
