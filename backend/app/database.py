"""Database configuration and session management"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - try PostgreSQL first, fallback to SQLite for easier setup
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    None
)

# If no DATABASE_URL set, use SQLite (easier for development)
if DATABASE_URL is None:
    # Use SQLite for easier setup - no PostgreSQL required
    DATABASE_URL = "sqlite:///./project_manager.db"
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    # Use PostgreSQL if DATABASE_URL is provided
    engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

