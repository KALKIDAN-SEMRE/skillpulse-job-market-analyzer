"""
Database configuration and session management.
Uses SQLite for simplicity in Day 1.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file location
SQLALCHEMY_DATABASE_URL = "sqlite:///./skillpulse.db"

# Create SQLAlchemy engine
# connect_args needed for SQLite to allow multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Used with FastAPI's Depends() for dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    Call this when starting the application.
    
    Note: Models must be imported before calling this function
    to register them with Base.metadata.
    """
    # Import models to ensure they're registered with Base.metadata
    from app import models  # noqa: F401
    
    Base.metadata.create_all(bind=engine)

