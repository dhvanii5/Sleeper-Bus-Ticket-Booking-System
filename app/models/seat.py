"""Database Models for Seat Management and Availability Tracking"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from datetime import datetime
from ..database import Base


class Seat(Base):
    """Master seat table - stores all physical seats on the bus"""
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, index=True)  # e.g., "S01", "S02" (user-friendly ID)
    seat_type = Column(String)  # "lower" or "upper" berth
    base_price = Column(Integer)  # Base fare for this seat type
    is_available = Column(Boolean, default=True)  # Seat operational status (not booking status)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeatAvailability(Base):
    """Tracks seat bookings for specific routes and dates (prevents double-booking)"""
    __tablename__ = "seat_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    seat_id = Column(Integer, ForeignKey('seats.id'))  # Which seat is booked
    from_station_id = Column(Integer, ForeignKey('stations.id'))  # Boarding station
    to_station_id = Column(Integer, ForeignKey('stations.id'))  # Alighting station
    journey_date = Column(Date)  # Date of travel
    is_booked = Column(Boolean, default=False)  # Booking status for this segment
    booked_by = Column(Integer, ForeignKey('bookings.id'), nullable=True)  # Link to booking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)