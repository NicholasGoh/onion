from fastapi import FastAPI

from app.container import Container
from app.database.config import create_db_and_tables
from app.routers import items

# Initialize DI container
container = Container()
container.wire(modules=["app.routers.items"])

app = FastAPI()
app.container = container

app.include_router(items.router)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup"""
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
