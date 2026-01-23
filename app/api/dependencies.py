"""API Dependencies - Shared Resources for Route Handlers

This module provides dependency injection functions that supply common
resources (like database sessions) to API endpoints in a clean way.

FastAPI's dependency injection system automatically calls these functions
and provides their return values to route handlers.
"""

# API dependencies
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal


def get_db():
    """
    Database Session Dependency - Provides a database connection to routes
    
    This function creates a new database session for each API request,
    yields it to the route handler, and ensures it's closed afterward
    (even if an exception occurs).
    
    The 'yield' keyword makes this a generator, allowing cleanup code
    after the route handler completes.
    
    Usage:
        @router.get("/bookings")
        def get_bookings(db: Session = Depends(get_db)):
            # 'db' is automatically injected here
            return db.query(Booking).all()
    
    Yields:
        Session: SQLAlchemy database session for this request
    """
    # Create a new session from our session factory
    db = SessionLocal()
    try:
        # Provide the session to the route handler
        yield db
    finally:
        # Cleanup: Always close the session when done
        # This returns the connection to the pool
        db.close()
