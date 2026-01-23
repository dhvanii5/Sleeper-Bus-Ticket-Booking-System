"""Database Models for Booking Management"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Booking(Base):
    """Main booking table - stores passenger reservations"""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, index=True)  # Human-readable ID (e.g., BUS-AHM-MUM-20260123-XYZW)
    pnr = Column(String, unique=True, index=True)  # 9-char alphanumeric PNR
    user_name = Column(String)  # Passenger name
    email = Column(String, index=True)  # For notifications and lookup
    phone = Column(String)  # Contact number (10 digits)
    from_station_id = Column(Integer, ForeignKey('stations.id'))  # Origin
    to_station_id = Column(Integer, ForeignKey('stations.id'))  # Destination
    booking_date = Column(String)  # When booking was made
    journey_date = Column(String)  # When travel will occur
    status = Column(String, default="CONFIRMED")  # CONFIRMED, CANCELLED, PENDING
    total_amount = Column(Integer)  # Total fare (seats + meals)
    refund_amount = Column(Integer, default=0)  # Amount refunded if cancelled
    confirmation_probability = Column(Float, default=0.0)  # ML prediction score
    created_at = Column(DateTime, default=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)  # Cancellation timestamp

    # Relationship: One booking can have multiple meals
    meals = relationship("BookingMeal", back_populates="booking")


class BookingMeal(Base):
    """Junction table linking bookings to meals (many-to-many relationship)"""
    __tablename__ = "booking_meals"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))  # Which booking
    meal_id = Column(Integer, ForeignKey('meals.id'))  # Which meal
    quantity = Column(Integer, default=1)  # How many of this meal
    customization = Column(String, nullable=True)  # Special requests (e.g., "no onions")

    # Bidirectional relationship with Booking
    booking = relationship("Booking", back_populates="meals")
