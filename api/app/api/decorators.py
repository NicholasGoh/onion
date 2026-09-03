import functools
import inspect

from fastapi import HTTPException, Request

from app.data.config import settings
from app.data.csrf import verify_csrf_token
from app.data.entities import Session
from app.data.infra.kratos_client import KRATOS_SESSION_COOKIE
from app.data.interfaces import IAuthClient

SESSION_TOKEN_HEADER = "X-Session-Token"
CSRF_TOKEN_HEADER = "X-CSRF-Token"


def _get_request(kwargs: dict) -> Request:
    request = kwargs.get("request")
    if request is None:
        raise TypeError(
            "authn-wrapped route must declare a `request: Request` parameter"
        )
    return request


def _get_auth_client(kwargs: dict) -> IAuthClient:
    auth_client = kwargs.get("auth_client")
    if auth_client is None:
        raise TypeError(
            "authn-wrapped route must declare an "
            "`auth_client: IAuthClient = Depends(Provide[Container.kratos_client])` parameter"
        )
    return auth_client


def _check_csrf(request: Request, session: Session) -> None:
    csrf_token = request.headers.get(CSRF_TOKEN_HEADER)
    if not csrf_token or not verify_csrf_token(
        session.id, csrf_token, settings.csrf_secret
    ):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")


def authn(fn):
    """Dual-transport: API clients authenticate with a Kratos session token
    in the X-Session-Token header (no CSRF risk - browsers never auto-attach
    arbitrary headers cross-site); browser clients authenticate with the
    Kratos session cookie, which additionally requires a valid X-CSRF-Token
    (api/'s own synchronizer token - Kratos's own csrf_token only protects
    its self-service flows, not downstream API routes).

    Also dual-mode on sync/async: dispatches based on whether the wrapped
    route is a coroutine function, so a blocking sync call never runs inside
    an async def route's event loop turn.

    Reads the Kratos client out of the route's own resolved kwargs (wired
    via the route's normal @inject/Depends(Provide[...]) params), rather
    than resolving it itself - this wrapper is a closure created fresh on
    every decoration, so it's never a module-level attribute that
    dependency_injector's wiring could discover and patch on its own.

    Apply below @inject, e.g.:

        @router.post("/quote")
        @inject
        @authn
        def quote_order(
            request: Request,
            order: OrderCreate,
            auth_client: IAuthClient = Depends(Provide[Container.kratos_client]),
            service: OrderService = Depends(Provide[Container.order_service]),
        ):
            ...
    """
    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def async_wrapper(*args, **kwargs):
            request = _get_request(kwargs)
            auth_client = _get_auth_client(kwargs)
            token = request.headers.get(SESSION_TOKEN_HEADER)
            if token:
                session = await auth_client.awhoami(token=token)
                if session is None:
                    raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                cookie = request.cookies.get(KRATOS_SESSION_COOKIE)
                session = await auth_client.awhoami(cookie=cookie) if cookie else None
                if session is None:
                    raise HTTPException(status_code=401, detail="Unauthorized")
                _check_csrf(request, session)
            return await fn(*args, **kwargs)

        return async_wrapper
    else:

        @functools.wraps(fn)
        def sync_wrapper(*args, **kwargs):
            request = _get_request(kwargs)
            auth_client = _get_auth_client(kwargs)
            token = request.headers.get(SESSION_TOKEN_HEADER)
            if token:
                session = auth_client.whoami(token=token)
                if session is None:
                    raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                cookie = request.cookies.get(KRATOS_SESSION_COOKIE)
                session = auth_client.whoami(cookie=cookie) if cookie else None
                if session is None:
                    raise HTTPException(status_code=401, detail="Unauthorized")
                _check_csrf(request, session)
            return fn(*args, **kwargs)

        return sync_wrapper
