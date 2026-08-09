from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/app"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
