from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: str
    phone: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StationBase(BaseModel):
    name: str
    arrival_time: str
    departure_time: str
    distance_km: int
    sequence: int


class StationCreate(StationBase):
    pass


class Station(StationBase):
    id: int

    class Config:
        from_attributes = True


class SeatBase(BaseModel):
    seat_number: str
    seat_type: str
    base_price: int
    is_available: bool = True


class SeatCreate(SeatBase):
    pass


class Seat(SeatBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookingMealBase(BaseModel):
    meal_id: int
    quantity: int = 1
    customization: Optional[str] = None


class MealBase(BaseModel):
    name: str
    description: str
    price: int
    category: str


class MealCreate(MealBase):
    pass


class Meal(MealBase):
    id: int
    is_available: bool

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    user_name: str
    email: str
    phone: str
    from_station_id: int
    to_station_id: int
    seat_id: int
    journey_date: str
    meals: Optional[list[int]] = None


class BookingCreate(BookingBase):
    pass


class Booking(BaseModel):
    id: int
    booking_reference: str
    user_name: str
    email: str
    phone: str
    from_station_id: int
    to_station_id: int
    seat_id: int
    booking_date: str
    journey_date: str
    status: str
    total_amount: int
    refund_amount: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookingCancellation(BaseModel):
    booking_reference: str
    refund_amount: int
    refund_percentage: int
    refund_status: str


class SeatAvailability(BaseModel):
    seat_id: int
    seat_number: str
    seat_type: str
    base_price: int
    calculated_price: int

    class Config:
        from_attributes = True


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