from fastapi import Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject

from app.container import Container
from app.data.config import settings
from app.data.csrf import verify_csrf_token
from app.data.entities import Session
from app.data.infra.kratos_client import KRATOS_SESSION_COOKIE
from app.data.interfaces import IAuthClient

SESSION_TOKEN_HEADER = "X-Session-Token"
CSRF_TOKEN_HEADER = "X-CSRF-Token"


def _check_csrf(request: Request, session: Session) -> None:
    csrf_token = request.headers.get(CSRF_TOKEN_HEADER)
    if not csrf_token or not verify_csrf_token(
        session.id, csrf_token, settings.csrf_secret
    ):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")


@inject
async def authn(
    request: Request,
    auth_client: IAuthClient = Depends(Provide[Container.kratos_client]),
) -> Session:
    """Dual-transport: API clients authenticate with a Kratos session token
    in the X-Session-Token header (no CSRF risk - browsers never auto-attach
    arbitrary headers cross-site); browser clients authenticate with the
    Kratos session cookie, which additionally requires a valid X-CSRF-Token
    (api/'s own synchronizer token - Kratos's own csrf_token only protects
    its self-service flows, not downstream API routes).

    Applied as a router-level dependency (see main.py's include_router calls)
    rather than a per-route decorator, so a new route can't be wired up
    without authn by omission.
    """
    token = request.headers.get(SESSION_TOKEN_HEADER)
    if token:
        session = await auth_client.awhoami(token=token)
        if session is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return session

    cookie = request.cookies.get(KRATOS_SESSION_COOKIE)
    session = await auth_client.awhoami(cookie=cookie) if cookie else None
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    _check_csrf(request, session)
    return session
