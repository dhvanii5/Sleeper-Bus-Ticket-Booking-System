TRAVEL_DATE = "2025-12-25"


def _create_booking(client, seed_data, *, seat_index=0, email="test@example.com"):
	payload = {
		"user_name": "Booking User",
		"email": email,
		"phone": "9876543210",
		"from_station_id": seed_data["stations"][0].id,
		"to_station_id": seed_data["stations"][4].id,
		"seat_id": seed_data["seats"][seat_index].id,
		"journey_date": TRAVEL_DATE,
	}
	return client.post("/api/v1/bookings/", json=payload)


def test_cancel_booking_releases_seat(client, seed_data):
	booking_resp = _create_booking(client, seed_data)
	assert booking_resp.status_code == 200
	booking_ref = booking_resp.json()["booking_reference"]

	cancel_resp = client.delete(f"/api/v1/bookings/{booking_ref}")
	assert cancel_resp.status_code == 200
	cancel_data = cancel_resp.json()
	assert cancel_data["refund_status"] in {"FULL_REFUND", "PARTIAL_REFUND", "NO_REFUND"}

	availability = client.get(
		"/api/v1/seats/availability",
		params={
			"from_station": seed_data["stations"][0].id,
			"to_station": seed_data["stations"][4].id,
			"travel_date": TRAVEL_DATE,
		},
	)
	assert availability.status_code == 200
	seats = {seat["seat_number"] for seat in availability.json()}
	assert "L01" in seats


def test_booking_history_lists_user_bookings(client, seed_data):
	email = "history@example.com"
	first = _create_booking(client, seed_data, seat_index=0, email=email)
	second = _create_booking(client, seed_data, seat_index=2, email=email)
	assert first.status_code == 200 and second.status_code == 200

	history = client.get(f"/api/v1/bookings/history/{email}")
	assert history.status_code == 200
	data = history.json()
	assert len(data) == 2
