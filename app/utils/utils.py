import re
from datetime import datetime, timedelta

# =============================================================================
# VALIDATION UTILITIES
# =============================================================================

def validate_email(email: str) -> bool:
    """Validate email format using regex pattern (simple validation)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number - must be exactly 10 digits"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def validate_station_combination(from_station_seq: int, to_station_seq: int) -> bool:
    """Ensure origin comes before destination in route (prevents backwards booking)"""
    return from_station_seq < to_station_seq

def validate_booking_date(booking_date: str) -> bool:
    """Check if date string is in valid YYYY-MM-DD format"""
    try:
        datetime.strptime(booking_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_seat_number(seat_number: str) -> bool:
    """Validate seat number format (e.g., S01, U12, L05)"""
    pattern = r'^[A-Z]\d{1,2}$'
    return re.match(pattern, seat_number) is not None

# =============================================================================
# PRICING & REFUND UTILITIES
# =============================================================================

def calculate_refund_amount(total_amount: int, journey_time: datetime, cancellation_time: datetime) -> dict:
    """
    Calculate refund based on cancellation timeline
    Policy: 100% (>=24h), 50% (>=12h), 0% (<12h)
    """
    # Calculate hours between cancellation and journey
    time_difference = journey_time - cancellation_time
    hours_difference = time_difference.total_seconds() / 3600

    # Apply refund policy based on timeline
    if hours_difference >= 24:
        refund_amount = total_amount
        refund_percentage = 100
        status = "FULL_REFUND"
    elif hours_difference >= 12:
        refund_amount = int(total_amount * 0.5)
        refund_percentage = 50
        status = "PARTIAL_REFUND"
    else:
        refund_amount = 0
        refund_percentage = 0
        status = "NO_REFUND"

    return {
        "refund_amount": refund_amount,
        "refund_percentage": refund_percentage,
        "status": status,
        "hours_before_journey": hours_difference
    }

def calculate_distance_between_stations(station1_km: int, station2_km: int) -> int:
    """Calculate absolute distance between two stations (in kilometers)"""
    return abs(station2_km - station1_km)

def get_distance_multiplier(distance_km: int) -> float:
    """
    Get pricing multiplier based on distance traveled
    Longer distances get higher multipliers (0-100km: 1.0x, 101-300km: 1.2x, >300km: 1.5x)
    """
    if distance_km <= 100:
        return 1.0
    elif distance_km <= 300:
        return 1.2
    else:
        return 1.5

def get_seat_type_multiplier(seat_type: str) -> float:
    """
    Calculate seat type pricing multiplier.
    - Upper Berth: 1.0x (Standard)
    - Lower Berth: 1.3x (Premium)
    """
    if seat_type.lower() == "lower":
        return 1.3
    return 1.0
