from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime, date
from typing import Optional, List

# Basic Models
class StationBase(BaseModel):
    name: str
    arrival_time: str
    departure_time: str
    distance_km: int
    sequence: int

class Station(StationBase):
    id: int
    class Config:
        from_attributes = True

class StationsResponse(BaseModel):
    route: str
    stations: List[Station]

class SeatBase(BaseModel):
    seat_number: str
    seat_type: str
    base_price: int
    is_available: bool = True

class Seat(SeatBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class MealBase(BaseModel):
    name: str
    description: str
    price: int
    category: str

class Meal(MealBase):
    id: int
    is_available: bool
    class Config:
        from_attributes = True

# Booking Request Models
class PassengerDetails(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    contact: str = Field(..., pattern=r'^\d{10}$')
    email: EmailStr

class MealItem(BaseModel):
    meal_id: int # Changed to int as our DB uses int
    quantity: int = Field(default=1, ge=1, le=10)

class BookingCreate(BaseModel):
    from_station: str
    to_station: str
    travel_date: date
    seats: List[int] = Field(..., min_items=1, max_items=5)
    passenger_details: PassengerDetails
    meals: Optional[List[MealItem]] = []

    @validator('travel_date')
    def validate_future_date(cls, v):
        if v < date.today():
            raise ValueError('Travel date must be in the future')
        return v

# Booking Response Models
class JourneyDetails(BaseModel):
    from_station: str
    to_station: str
    date: date
    departure_time: str
    arrival_time: str
    duration: str = "TBD"

class BookingResponse(BaseModel):
    booking_id: str
    pnr: str
    status: str
    total_amount: float
    confirmation_probability: float
    seats: List[str]
    meals: List[MealItem]
    journey_details: JourneyDetails
    passenger_details: PassengerDetails
    created_at: datetime

class BookingCancellation(BaseModel):
    booking_reference: str
    refund_amount: int
    refund_percentage: int
    refund_status: str

class PredictionRequest(BaseModel):
    booking_reference: str
    user_name: str
    email: str
    phone: str
    from_station_id: int
    to_station_id: int

class PredictionResponse(BaseModel):
    booking_reference: str
    confirmation_probability: float
    cancellation_risk: float
    no_show_risk: float
    recommendation: str