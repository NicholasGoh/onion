from fastapi import FastAPI

from app.api import routes
from app.container import Container
from app.data.config import create_db_and_tables

container = Container()
container.wire(modules=["app.api.routes"])

app = FastAPI()
app.container = container

app.include_router(routes.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
