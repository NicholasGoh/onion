from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/app"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session
