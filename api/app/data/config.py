from pydantic_settings import BaseSettings
from sqlmodel import Session, SQLModel, create_engine


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@postgres:5432/app"
    test_db_name: str = "test_app"


settings = Settings()
DATABASE_URL = settings.database_url


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
