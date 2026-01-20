import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None


def validate_station_combination(from_station_seq: int, to_station_seq: int) -> bool:
    """Validate that from_station comes before to_station"""
    return from_station_seq < to_station_seq


def validate_booking_date(booking_date: str) -> bool:
    """Validate booking date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(booking_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_seat_number(seat_number: str) -> bool:
    """Validate seat number format"""
    pattern = r'^[A-Z]\d{1,2}$'  # A1, B12, etc.
    return re.match(pattern, seat_number) is not None
