from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from typing import Generator

# Database URL
DATABASE_URL = "mysql+pymysql://root:pass@localhost:3306/stock_database"

# Create the engine
engine = create_engine(DATABASE_URL)

# Configure session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for ORM models
@as_declarative()
class Base:
    id: any
    __name__: str

    # Automatically generate table names
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# Dependency for FastAPI routes
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
