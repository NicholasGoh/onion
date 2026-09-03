from pydantic_settings import BaseSettings
from sqlmodel import Session, SQLModel, create_engine


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@postgres:5432/app"
    test_db_name: str = "test_app"
    kratos_public_url: str = "http://kratos:4433"
    csrf_secret: str = "insecure-dev-secret-change-in-production"


settings = Settings()
DATABASE_URL = settings.database_url


def get_engine():
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )
    yield engine
    engine.dispose()


def get_session(engine):
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
