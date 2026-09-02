import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/app"
)


def get_engine():
    engine = create_engine(DATABASE_URL, echo=True)
    yield engine
    engine.dispose()


def get_session(engine):
    session = Session(engine)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
