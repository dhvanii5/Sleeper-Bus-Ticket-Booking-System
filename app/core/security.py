import random
import string
from datetime import datetime


def generate_booking_reference(from_station: str, to_station: str) -> str:
    """
    Generate unique booking reference in format: BUS-FROM-TO-DATE-RANDOM
    Example: BUS-AHM-MUM-20250125-A1B2
    """
    date_str = datetime.now().strftime("%Y%m%d")
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"BUS-{from_station[:3].upper()}-{to_station[:3].upper()}-{date_str}-{random_code}"
