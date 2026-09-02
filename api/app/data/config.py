import os

from sqlmodel import SQLModel, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/app"
)


def get_engine():
    engine = create_engine(DATABASE_URL, echo=True)
    yield engine
    engine.dispose()


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
