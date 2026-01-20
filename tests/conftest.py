import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_db
from app.database import Base
from app.main import app
from app.models.booking import Booking, BookingMeal
from app.models.meal import Meal
from app.models.seat import Seat, SeatAvailability
from app.models.station import Station


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_data(db_session):
    stations = [
        Station(name="Ahmedabad", arrival_time="08:00", departure_time="08:30", distance_km=0, sequence=1),
        Station(name="Vadodara", arrival_time="10:15", departure_time="10:30", distance_km=110, sequence=2),
        Station(name="Surat", arrival_time="12:15", departure_time="12:30", distance_km=220, sequence=3),
        Station(name="Vapi", arrival_time="14:00", departure_time="14:10", distance_km=300, sequence=4),
        Station(name="Mumbai", arrival_time="17:30", departure_time="--", distance_km=370, sequence=5),
    ]
    seats = [
        Seat(seat_number="L01", seat_type="lower", base_price=500, is_available=True),
        Seat(seat_number="U01", seat_type="upper", base_price=450, is_available=True),
        Seat(seat_number="L02", seat_type="lower", base_price=500, is_available=True),
    ]
    meals = [
        Meal(name="Veg Thali", description="Dal, sabzi, roti", price=120, category="VEG"),
        Meal(name="Paneer Wrap", description="Paneer tikka wrap", price=90, category="VEG"),
        Meal(name="Chicken Biryani", description="Spiced rice with chicken", price=150, category="NON_VEG"),
    ]

    db_session.add_all(stations + seats + meals)
    db_session.commit()

    return {
        "stations": stations,
        "seats": seats,
        "meals": meals,
    }
