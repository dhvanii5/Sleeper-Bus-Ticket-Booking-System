from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from ..database import Base


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, index=True)
    user_name = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    from_station_id = Column(Integer, ForeignKey('stations.id'))
    to_station_id = Column(Integer, ForeignKey('stations.id'))
    seat_id = Column(Integer, ForeignKey('seats.id'))
    booking_date = Column(String)
    journey_date = Column(String)
    status = Column(String, default="CONFIRMED")  # CONFIRMED, CANCELLED, PENDING
    total_amount = Column(Integer)
    refund_amount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)


class BookingMeal(Base):
    __tablename__ = "booking_meals"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'))
    quantity = Column(Integer, default=1)
    customization = Column(String, nullable=True)
