"""Database Connection and Session Management

This module sets up the SQLAlchemy database engine and session factory.

Components:
- engine: The database connection pool (reusable connections)
- SessionLocal: Factory for creating database sessions (one per request)
- Base: Parent class for all database models (tables)

Usage:
    from app.database import SessionLocal, Base
    db = SessionLocal()  # Create a new session
    # ... perform database operations ...
    db.close()  # Always close when done
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

# Create the database engine - manages connection pooling
# echo=False means don't log SQL queries (set True for debugging)
engine = create_engine(DATABASE_URL)

# Session factory - creates individual database sessions
# autocommit=False: Changes must be explicitly committed
# autoflush=False: Changes aren't automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models - inherit from this to create tables
Base = declarative_base()