from datetime import datetime, timedelta


def calculate_refund_amount(total_amount: int, booking_time: datetime, cancellation_time: datetime) -> dict:
    """
    Calculate refund amount based on cancellation policy
    - Full refund if cancelled 24hrs before
    - 50% if 12-24hrs before
    - No refund if less than 12hrs
    """
    time_difference = booking_time - cancellation_time
    hours_difference = time_difference.total_seconds() / 3600

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
    """Calculate distance between two stations"""
    return abs(station2_km - station1_km)


def get_distance_multiplier(distance_km: int) -> float:
    """
    Calculate distance-based pricing multiplier
    Base: 0-100km = 1.0x
    100-300km = 1.2x
    300km+ = 1.5x
    """
    if distance_km <= 100:
        return 1.0
    elif distance_km <= 300:
        return 1.2
    else:
        return 1.5


def get_seat_type_multiplier(seat_type: str) -> float:
    """
    Calculate seat type pricing multiplier
    Upper berth: 1.0x
    Lower berth: 1.3x (premium)
    """
    if seat_type.lower() == "lower":
        return 1.3
    return 1.0
