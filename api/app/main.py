from fastapi import FastAPI

from app.api.items import routes as item_routes
from app.api.orders import routes as order_routes
from app.api.tags import routes as tag_routes
from app.container import Container
from app.data.config import create_db_and_tables

container = Container()
container.wire(modules=["app.api.items.routes", "app.api.orders.routes", "app.api.tags.routes"])

app = FastAPI()
app.container = container

app.include_router(item_routes.router)
app.include_router(order_routes.router)
app.include_router(tag_routes.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
