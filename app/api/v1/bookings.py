from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...api.dependencies import get_db
from ...services.booking_service import BookingService
from ...schemas.seat import Booking, BookingCreate, BookingCancellation

router = APIRouter()


@router.post("/", response_model=Booking)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking
    
    Body:
    - user_name: Passenger name
    - email: Passenger email
    - phone: Passenger phone (10 digits)
    - from_station_id: Starting station ID
    - to_station_id: Destination station ID
    - seat_id: Seat to book
    - journey_date: Travel date in YYYY-MM-DD format
    - meals: Optional list of meal IDs to add
    """
    new_booking = BookingService.create_booking(
        db,
        booking.user_name,
        booking.email,
        booking.phone,
        booking.from_station_id,
        booking.to_station_id,
        booking.seat_id,
        booking.journey_date,
        booking.meals
    )
    return new_booking


@router.get("/{booking_reference}", response_model=Booking)
async def get_booking(
    booking_reference: str,
    db: Session = Depends(get_db)
):
    """Get booking details by booking reference"""
    booking = BookingService.get_booking_details(db, booking_reference)
    return booking


@router.get("/history/{email}")
async def get_booking_history(
    email: str,
    db: Session = Depends(get_db)
):
    """Get all bookings for a user by email"""
    bookings = BookingService.get_booking_history(db, email)
    return bookings


@router.delete("/{booking_reference}", response_model=BookingCancellation)
async def cancel_booking(
    booking_reference: str,
    db: Session = Depends(get_db)
):
    """
    Cancel a booking
    
    Refund policy:
    - Full refund if cancelled 24+ hours before journey
    - 50% refund if cancelled 12-24 hours before journey
    - No refund if cancelled less than 12 hours before journey
    """
    cancellation_info = BookingService.cancel_booking(db, booking_reference)
    return cancellation_info


@router.put("/{booking_reference}/meals")
async def update_booking_meals(
    booking_reference: str,
    meal_ids: List[int],
    db: Session = Depends(get_db)
):
    """
    Update meal selection for an existing booking
    
    Body: List of meal IDs
    """
    updated_booking = BookingService.update_booking_meals(
        db, booking_reference, meal_ids
    )
    return updated_booking
