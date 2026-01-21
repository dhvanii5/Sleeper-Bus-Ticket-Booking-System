import sys
from pathlib import Path
from fastapi.testclient import TestClient
import json

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.main import app

client = TestClient(app)

def print_result(name, passed, details=None):
    status = "PASS" if passed else "FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"   {details}")

def verify_refactor():
    print("="*50)
    print("Verifying Sleeper Bus Refactor")
    print("="*50)
    
    # 1. Verify Seats
    try:
        response = client.get("/api/v1/seats/?from=Ahmedabad&to=Mumbai&date=2026-01-25")
        if response.status_code == 200:
            data = response.json()
            seats = data.get("seats", [])
            print_result("Get Seats (Query Params)", True, f"Found {len(seats)} seats")
            if len(seats) == 40:
                print_result("Seat Count is 40", True)
            else:
                print_result("Seat Count is 40", False, f"Actual: {len(seats)}")
        else:
            print_result("Get Seats (Query Params)", False, f"Status: {response.status_code} {response.text}")
    except Exception as e:
        print_result("Get Seats", False, str(e))

    # 2. Verify Stations
    try:
        response = client.get("/api/v1/stations") # Endpoint changed
        if response.status_code == 200:
            data = response.json()
            # Expecting { "route": "...", "stations": [...] }
            if "route" in data and "stations" in data:
                 print_result("Get Stations (Wrapped Structure)", True, "Route key present")
                 stations = data["stations"]
                 names = [s["name"] for s in stations]
                 expected = ["Ahmedabad", "Vadodara", "Surat", "Vapi", "Mumbai"]
                 if names == expected:
                     print_result("Stations Match Expected", True)
                 else:
                     print_result("Stations Match Expected", False, f"Actual: {names}")
            else:
                 print_result("Get Stations Structure", False, "Missing route or stations key")
        else:
            print_result("Get Stations", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Get Stations", False, str(e))

    # 3. Verify Meals
    try:
        response = client.get("/api/v1/meals/")
        if response.status_code == 200:
            meals = response.json()
            print_result("Get Meals", True, f"Found {len(meals)} meals")
            if len(meals) > 0:
                print_result("Meals Exist", True)
        else:
            print_result("Get Meals", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Get Meals", False, str(e))

    # 4. Verify Create Booking (Multiple Seats)
    try:
        # Get seats (Assuming S01=1, S02=2)
        # We need IDs. We assume 1 -> S01, 2 -> S02 from seeding
        seat_ids = [1, 2] 
        
        # Get meal ID
        meals_res = client.get("/api/v1/meals/").json()
        meal_id = meals_res[0]["id"]
        
        booking_payload = {
            "from_station": "Ahmedabad", # Changed to name as per schema? No, service expects name, schema expects string.
            # Wait, schemas/seat.py BookingCreate uses from_station: str.
            # And BookingService uses name to lookup.
            # So we pass Names "Ahmedabad", "Mumbai"
            "to_station": "Mumbai",
            "travel_date": "2026-01-25",
            "seats": seat_ids, # List of ints
            "passenger_details": {
                "name": "Test Group",
                "email": "group@example.com",
                "contact": "9876543210"
            },
            "meals": [
                {"meal_id": meal_id, "quantity": 2}
            ]
        }
        
        print("\nSending Booking Payload:", json.dumps(booking_payload, indent=2))
        
        response = client.post("/api/v1/bookings/", json=booking_payload)
        
        if response.status_code == 200:
            data = response.json()
            print_result("Create Booking", True, f"Booking ID: {data.get('booking_id')}")
            
            # Verify confirmation_probability
            if "confirmation_probability" in data:
                print_result("Has Confirmation Probability", True, f"Value: {data['confirmation_probability']}")
            else:
                print_result("Has Confirmation Probability", False)

            # Verify seats list
            if "seats" in data and len(data["seats"]) == 2:
                print_result("Multiple Seats Booked", True, f"Seats: {data['seats']}")
            else:
                print_result("Multiple Seats Booked", False, f"Got: {data.get('seats')}")
                
            # Verify Meals in response
            if "meals" in data and len(data["meals"]) > 0:
                print_result("Has Meals in Response", True)
            else:
                print_result("Has Meals in Response", False)
                
        else:
            print_result("Create Booking", False, f"Status: {response.status_code} {response.text}")
            
    except Exception as e:
        print_result("Create Booking", False, str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_refactor()
