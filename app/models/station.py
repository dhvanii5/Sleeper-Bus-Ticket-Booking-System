"""Database Model for Bus Route Stations"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base


class Station(Base):
    """Represents a stop on the bus route with timing and position info"""
    __tablename__ = "stations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Station name (e.g., "Ahmedabad")
    arrival_time = Column(String)  # Time bus arrives (e.g., "20:15")
    departure_time = Column(String)  # Time bus departs (e.g., "20:30")
    distance_km = Column(Integer)  # Distance from starting point in kilometers
    sequence = Column(Integer, unique=True)  # Position in route (1=origin, 2,3... n=destination)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
