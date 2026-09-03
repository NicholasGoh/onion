from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.api.decorators import authn
from app.api.items import routes as item_routes
from app.api.orders import routes as order_routes
from app.api.tags import routes as tag_routes
from app.container import Container
from app.data.config import create_db_and_tables

container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    container.init_resources()
    create_db_and_tables(container.db_engine())
    yield
    container.shutdown_resources()


app = FastAPI(lifespan=lifespan)
app.container = container


@app.middleware("http")
async def scope_db_session(request, call_next):
    try:
        return await call_next(request)
    finally:
        container.db_session.shutdown()


app.include_router(item_routes.router, dependencies=[Depends(authn)])
app.include_router(order_routes.router, dependencies=[Depends(authn)])
app.include_router(tag_routes.router, dependencies=[Depends(authn)])


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
