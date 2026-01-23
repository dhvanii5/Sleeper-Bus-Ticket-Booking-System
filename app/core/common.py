"""Core Business Logic - Common Utilities and Domain Exceptions

This module contains:
1. Custom HTTP exception classes for domain-specific errors
2. Utility functions for generating booking identifiers

All exceptions inherit from FastAPI's HTTPException, which automatically
converts them to proper HTTP error responses with status codes.
"""

import random
import string
from datetime import datetime
from fastapi import HTTPException, status

# =============================================================================
# CUSTOM EXCEPTIONS (Domain-Specific HTTP Errors)
# =============================================================================
# These exceptions represent business rule violations. When raised, FastAPI
# automatically converts them to HTTP error responses with the specified
# status code and detail message.

class SeatNotAvailableException(HTTPException):
    """
    Raised when a seat doesn't exist or is not in service
    
    HTTP Status: 400 Bad Request
    Use cases:
        - Seat number doesn't exist (e.g., "S99")
        - Seat is marked as out-of-service/maintenance
    """
    def __init__(self, detail: str = "Seat is not available for the selected route"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class BookingNotFoundException(HTTPException):
    """
    Raised when a booking reference cannot be found in the database
    
    HTTP Status: 404 Not Found
    Use cases:
        - Invalid booking reference provided
        - Trying to access a deleted/non-existent booking
    """
    def __init__(self, detail: str = "Booking not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InvalidStationException(HTTPException):
    """
    Raised when station combination is invalid or illogical
    
    HTTP Status: 400 Bad Request
    Use cases:
        - Station name doesn't exist
        - Reverse route (e.g., Mumbai → Ahmedabad when only AHM → MUM runs)
        - Same origin and destination
    """
    def __init__(self, detail: str = "Invalid station combination"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class CancellationNotAllowedException(HTTPException):
    """
    Raised when a booking cannot be cancelled
    
    HTTP Status: 400 Bad Request
    Use cases:
        - Booking already cancelled
        - Journey already completed
        - Too close to departure time (past cancellation deadline)
    """
    def __init__(self, detail: str = "Cancellation is not allowed for this booking"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class DoubleBookingException(HTTPException):
    """
    Raised when attempting to book a seat that's already reserved
    
    HTTP Status: 409 Conflict
    This prevents race conditions where multiple users try to book
    the same seat simultaneously.
    """
    def __init__(self, detail: str = "Seat is already booked for this route segment"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class InvalidBookingException(HTTPException):
    """
    Raised when booking data violates business rules
    
    HTTP Status: 400 Bad Request
    Use cases:
        - Invalid date format
        - Past travel date
        - Too many seats requested
        - Invalid passenger details
    """
    def __init__(self, detail: str = "Invalid booking details"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

# =============================================================================
# BOOKING IDENTIFIER GENERATORS
# =============================================================================
# These functions create unique, human-readable identifiers for bookings

def generate_booking_reference(from_station: str, to_station: str) -> str:
    """
    Generate unique booking reference in format: BUS-FROM-TO-DATE-RANDOM
    
    This creates a booking ID that is:
    - Unique: Timestamp + random suffix prevents collisions
    - Informative: Contains route info at a glance  
    - User-friendly: Easy to share over phone or email
    
    Format breakdown:
        BUS: Service type identifier
        FROM: First 3 letters of origin station (e.g., AHM for Ahmedabad)
        TO: First 3 letters of destination (e.g., MUM for Mumbai)
        DATE: Creation date in YYYYMMDD format
        RANDOM: 4-character random suffix for uniqueness
    
    Args:
        from_station: Name of origin station
        to_station: Name of destination station
    
    Returns:
        str: Booking reference like "BUS-AHM-MUM-20250121-A1B2"
    
    Example:
        >>> generate_booking_reference("Ahmedabad", "Mumbai")
        'BUS-AHM-MUM-20260123-X7Y9'
    """
    # Current date in compact format (YYYYMMDD)
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Random 4-character code for uniqueness
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # Combine all parts: service-origin-dest-date-random
    return f"BUS-{from_station[:3].upper()}-{to_station[:3].upper()}-{date_str}-{random_code}"

def generate_pnr() -> str:
    """
    Generate a 9-character Passenger Name Record (PNR) number
    
    PNR serves as a shorter, secondary identifier similar to airline tickets.
    It's easier to type on mobile and share verbally.
    
    Format: 9 random alphanumeric characters (A-Z, 0-9)
    Example: "7JV418ZCO"
    
    Returns:
        str: 9-character alphanumeric PNR
        
    Note:
        With 36 possible characters and 9 positions, there are
        36^9 ≈ 101 trillion possible combinations, ensuring uniqueness.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
