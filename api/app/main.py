from contextlib import asynccontextmanager

from fastapi import FastAPI

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

app.include_router(item_routes.router)
app.include_router(order_routes.router)
app.include_router(tag_routes.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
