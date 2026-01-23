"""Pydantic Schemas - API Request/Response Models with Validation"""

from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime, date
from typing import Optional, List

# =============================================================================
# STATION SCHEMAS
# =============================================================================

class StationBase(BaseModel):
    """Base fields for station data"""
    name: str
    arrival_time: str
    departure_time: str
    distance_km: int  # Distance from origin
    sequence: int  # Position in route (1, 2, 3...)

class Station(StationBase):
    """Station with database ID (for responses)"""
    id: int
    class Config:
        from_attributes = True  # Allow creating from ORM models

class StationsResponse(BaseModel):
    """Response for listing all stations on a route"""
    route: str
    stations: List[Station]

# =============================================================================
# SEAT SCHEMAS
# =============================================================================

class SeatBase(BaseModel):
    """Base fields for seat data"""
    seat_number: str  # e.g., "S02", "S10"
    seat_type: str  # "lower" or "upper"
    base_price: int
    is_available: bool = True  # Operational status

class Seat(SeatBase):
    """Seat with database ID and timestamps"""
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# =============================================================================
# MEAL SCHEMAS
# =============================================================================

class MealBase(BaseModel):
    """Base fields for meal data"""
    name: str
    description: str
    price: int
    category: str  # VEG, NON_VEG, DESSERT, BEVERAGE

class Meal(MealBase):
    """Meal with database ID and availability"""
    id: int
    is_available: bool
    class Config:
        from_attributes = True

# =============================================================================
# BOOKING REQUEST SCHEMAS
# =============================================================================

class PassengerDetails(BaseModel):
    """Passenger information for booking"""
    name: str = Field(..., min_length=2, max_length=100)
    contact: str = Field(..., pattern=r'^\d{10}$')  # Exactly 10 digits
    email: EmailStr  # Auto-validated email format

class MealItem(BaseModel):
    """Meal selection with quantity"""
    meal_id: int  # Reference to Meal table
    quantity: int = Field(default=1, ge=1, le=10)  # Min 1, max 10

class BookingCreate(BaseModel):
    """Request payload for creating a new booking"""
    from_station: str  # Station name (e.g., "Ahmedabad")
    to_station: str  # Station name (e.g., "Mumbai")
    travel_date: date  # Journey date
    seats: List[str] = Field(..., min_items=1, max_items=5, description="List of seat numbers (e.g., ['S02', 'S10'])")  # 1-5 seats
    passenger_details: PassengerDetails
    meals: Optional[List[MealItem]] = []  # Optional meal selection

    @validator('travel_date')
    def validate_future_date(cls, v):
        """Ensure travel date is not in the past"""
        if v < date.today():
            raise ValueError('Travel date must be in the future')
        return v

# =============================================================================
# BOOKING RESPONSE SCHEMAS
# =============================================================================
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
    # Backward-compatible metadata (optional)
    booking_reference: Optional[str] = None
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    from_station_id: Optional[int] = None
    to_station_id: Optional[int] = None

    # Feature inputs (defaults allow lighter payloads)
    days_before_journey: int = Field(3, ge=0, le=365)
    current_occupancy_percent: int = Field(70, ge=0, le=100)
    seat_type: str = Field("lower", pattern='^(upper|middle|lower)$')
    route_type: str = Field("full", pattern='^(full|partial)$')
    day_of_week: str = Field("Friday", pattern='^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$')
    seats_requested: int = Field(1, ge=1, le=10)
    is_holiday_season: bool = False
    booking_hour: int = Field(12, ge=0, le=23)


class PredictionFactors(BaseModel):
    lead_time: str
    occupancy: str
    seat_preference: str
    holiday_season: str
    route_profile: str
    booking_time: str
    party_size: str


class PredictionResponse(BaseModel):
    confirmation_probability: float
    cancellation_risk: float
    recommendation: str
    factors: PredictionFactors