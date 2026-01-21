import random
import string
from datetime import datetime
from fastapi import HTTPException, status

# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================

class SeatNotAvailableException(HTTPException):
    def __init__(self, detail: str = "Seat is not available for the selected route"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class BookingNotFoundException(HTTPException):
    def __init__(self, detail: str = "Booking not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InvalidStationException(HTTPException):
    def __init__(self, detail: str = "Invalid station combination"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class CancellationNotAllowedException(HTTPException):
    def __init__(self, detail: str = "Cancellation is not allowed for this booking"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class DoubleBookingException(HTTPException):
    def __init__(self, detail: str = "Seat is already booked for this route segment"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class InvalidBookingException(HTTPException):
    def __init__(self, detail: str = "Invalid booking details"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

# =============================================================================
# SECURITY & REFERENCE UTILITIES
# =============================================================================

def generate_booking_reference(from_station: str, to_station: str) -> str:
    """
    Generate unique booking reference in format: BUS-FROM-TO-DATE-RANDOM
    Example: BUS-AHM-MUM-20250121-A1B2
    """
    date_str = datetime.now().strftime("%Y%m%d")
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"BUS-{from_station[:3].upper()}-{to_station[:3].upper()}-{date_str}-{random_code}"

def generate_pnr() -> str:
    """Generate a random 9-character alphanumeric PNR"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
