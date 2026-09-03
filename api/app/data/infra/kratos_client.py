import httpx

from app.data.entities import Session
from app.data.interfaces import IAuthClient

KRATOS_SESSION_COOKIE = "ory_kratos_session"
KRATOS_SESSION_TOKEN_HEADER = "X-Session-Token"


def _session_from_response(resp: httpx.Response) -> Session | None:
    if resp.status_code != 200:
        return None
    body = resp.json()
    return Session(identity_id=body["identity"]["id"], id=body["id"])


class KratosClient(IAuthClient):

    def __init__(self, base_url: str):
        self._sync_client = httpx.Client(base_url=base_url)
        self._async_client = httpx.AsyncClient(base_url=base_url)

    def whoami(
        self, cookie: str | None = None, token: str | None = None
    ) -> Session | None:
        resp = self._sync_client.get(
            "/sessions/whoami",
            cookies={KRATOS_SESSION_COOKIE: cookie} if cookie else None,
            headers={KRATOS_SESSION_TOKEN_HEADER: token} if token else None,
        )
        return _session_from_response(resp)

    async def awhoami(
        self, cookie: str | None = None, token: str | None = None
    ) -> Session | None:
        resp = await self._async_client.get(
            "/sessions/whoami",
            cookies={KRATOS_SESSION_COOKIE: cookie} if cookie else None,
            headers={KRATOS_SESSION_TOKEN_HEADER: token} if token else None,
        )
        return _session_from_response(resp)
