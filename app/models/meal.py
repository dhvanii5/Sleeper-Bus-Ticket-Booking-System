"""Database Model for Meal Options"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..database import Base


class Meal(Base):
    """Represents food items available for booking (optional add-on)"""
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Meal name (e.g., "Veg Thali")
    description = Column(String)  # Details about the meal
    price = Column(Integer)  # Price in rupees
    category = Column(String)  # VEG, NON_VEG, DESSERT, BEVERAGE
    is_available = Column(Boolean, default=True)  # In stock or temporarily unavailable
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
