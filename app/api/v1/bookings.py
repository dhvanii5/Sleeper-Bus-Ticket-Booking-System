"""Booking API Endpoints - Handle ticket reservations and cancellations"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...api.dependencies import get_db
from ...services.booking_service import BookingService
from ...schemas.schemas import BookingResponse, BookingCreate, BookingCancellation

router = APIRouter()


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create new booking - validates availability, calculates price, generates booking reference
    Returns booking details with confirmation probability from ML model
    """
    # Create booking in database (handles seat blocking, price calculation)
    new_booking = BookingService.create_booking(db, booking)
    
    # Convert DB model to API response format (includes enriched data like seat numbers, journey details)
    return BookingService.get_booking_response_object(db, new_booking.id)


@router.get("/{booking_reference}", response_model=BookingResponse)
async def get_booking(
    booking_reference: str,
    db: Session = Depends(get_db)
):
    """Fetch booking details using booking reference (e.g., BUS-AHM-MUM-20260123-XYZW)"""
    # Retrieve booking from database
    booking = BookingService.get_booking_details(db, booking_reference)
    
    # Format and return enriched response
    return BookingService.get_booking_response_object(db, booking.id)


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
