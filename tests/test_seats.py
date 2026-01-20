from app.models.seat import SeatAvailability


TRAVEL_DATE = "2025-12-25"


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Welcome")


def test_get_stations(client, seed_data):
    response = client.get("/api/v1/stations/")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_seat_availability_lists_available(client, seed_data):
    response = client.get(
        "/api/v1/seats/availability",
        params={
            "from_station": seed_data["stations"][0].id,
            "to_station": seed_data["stations"][4].id,
            "travel_date": TRAVEL_DATE,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    seat_numbers = {item["seat_number"] for item in data}
    assert "L01" in seat_numbers and "U01" in seat_numbers


def test_booking_creation_blocks_seat(client, seed_data, db_session):
    payload = {
        "user_name": "Test User",
        "email": "test@example.com",
        "phone": "9876543210",
        "from_station_id": seed_data["stations"][0].id,
        "to_station_id": seed_data["stations"][4].id,
        "seat_id": seed_data["seats"][0].id,
        "journey_date": TRAVEL_DATE,
    }

    resp = client.post("/api/v1/bookings/", json=payload)
    assert resp.status_code == 200
    booking_ref = resp.json()["booking_reference"]
    assert booking_ref.startswith("BUS-")

    # Seat is blocked
    blocked = db_session.query(SeatAvailability).filter_by(seat_id=payload["seat_id"]).all()
    assert len(blocked) == 1


def test_overlapping_booking_prevented(client, seed_data):
    base_payload = {
        "user_name": "Overlap One",
        "email": "one@example.com",
        "phone": "9876543210",
        "from_station_id": seed_data["stations"][0].id,
        "to_station_id": seed_data["stations"][3].id,
        "seat_id": seed_data["seats"][1].id,
        "journey_date": TRAVEL_DATE,
    }
    first = client.post("/api/v1/bookings/", json=base_payload)
    assert first.status_code == 200

    # Overlapping route with same seat should conflict
    overlap_payload = {
        **base_payload,
        "user_name": "Overlap Two",
        "email": "two@example.com",
        "from_station_id": seed_data["stations"][1].id,
        "to_station_id": seed_data["stations"][4].id,
    }
    second = client.post("/api/v1/bookings/", json=overlap_payload)
    assert second.status_code == 409
    assert "already booked" in second.json()["detail"]
