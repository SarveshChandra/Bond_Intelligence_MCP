from collections.abc import Generator

# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# Database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Session local configuration
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

# Base class for declarative models
class Base(DeclarativeBase):
    pass

# Dependency to get a database session
def get_db() -> Generator[Session, None, None]:
    # Create a new database session
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()