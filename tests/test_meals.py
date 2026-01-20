TRAVEL_DATE = "2025-12-25"


def _create_booking(client, seed_data):
	payload = {
		"user_name": "Meal User",
		"email": "meal@example.com",
		"phone": "9876543210",
		"from_station_id": seed_data["stations"][0].id,
		"to_station_id": seed_data["stations"][4].id,
		"seat_id": seed_data["seats"][0].id,
		"journey_date": TRAVEL_DATE,
	}
	return client.post("/api/v1/bookings/", json=payload)


def test_list_available_meals(client, seed_data):
	resp = client.get("/api/v1/meals/")
	assert resp.status_code == 200
	meals = resp.json()
	assert len(meals) >= 3
	categories = {m["category"] for m in meals}
	assert "VEG" in categories


def test_update_booking_meals_adds_cost(client, seed_data):
	booking_resp = _create_booking(client, seed_data)
	assert booking_resp.status_code == 200
	booking_data = booking_resp.json()
	initial_total = booking_data["total_amount"]

	meal_id = seed_data["meals"][0].id
	update_resp = client.put(
		f"/api/v1/bookings/{booking_data['booking_reference']}/meals",
		json=[meal_id],
	)
	assert update_resp.status_code == 200
	updated = update_resp.json()
	assert updated["total_amount"] == initial_total + seed_data["meals"][0].price
