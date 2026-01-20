from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base


class Station(Base):
    __tablename__ = "stations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    arrival_time = Column(String)
    departure_time = Column(String)
    distance_km = Column(Integer)
    sequence = Column(Integer, unique=True)  # Order in the route
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
