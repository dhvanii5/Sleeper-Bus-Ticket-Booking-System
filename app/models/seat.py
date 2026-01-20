from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from datetime import datetime
from ..database import Base


class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, index=True)
    seat_type = Column(String)  # LOWER, UPPER
    base_price = Column(Integer)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeatAvailability(Base):
    __tablename__ = "seat_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    seat_id = Column(Integer, ForeignKey('seats.id'))
    from_station_id = Column(Integer, ForeignKey('stations.id'))
    to_station_id = Column(Integer, ForeignKey('stations.id'))
    journey_date = Column(Date)
    is_booked = Column(Boolean, default=False)
    booked_by = Column(Integer, ForeignKey('bookings.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)