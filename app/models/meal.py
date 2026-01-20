from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..database import Base


class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    category = Column(String)  # VEG, NON_VEG, DESSERT, BEVERAGE
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
