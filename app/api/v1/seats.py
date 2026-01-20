from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ...api.dependencies import get_db
from ...services.seat_service import SeatService
from ...services.station_service import StationService
from ...schemas.seat import Seat, SeatAvailability

router = APIRouter()


@router.get("/availability")
async def get_seat_availability(
    from_station: int = Query(..., description="From station ID"),
    to_station: int = Query(..., description="To station ID"),
    travel_date: str = Query(..., description="Travel date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Get available seats for a specific route and date
    
    Query parameters:
    - from_station: Station ID to depart from
    - to_station: Station ID to arrive at
    - travel_date: Date of travel in YYYY-MM-DD format
    """
    available_seats = SeatService.get_available_seats(
        db, from_station, to_station, travel_date
    )
    
    # Calculate price for each seat
    result = []
    for seat in available_seats:
        price = SeatService.calculate_seat_price(db, seat.id, from_station, to_station)
        result.append({
            "seat_id": seat.id,
            "seat_number": seat.seat_number,
            "seat_type": seat.seat_type,
            "base_price": seat.base_price,
            "calculated_price": price
        })
    
    return result


@router.get("/{seat_id}")
async def get_seat(seat_id: int, db: Session = Depends(get_db)):
    """Get seat details by ID"""
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if not seat:
        return {"error": "Seat not found"}
    return seat
