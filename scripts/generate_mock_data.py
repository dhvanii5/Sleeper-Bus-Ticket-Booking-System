import csv
import random

def generate_mock_data(filename, num_records=450):
    headers = [
        "booking_id", "days_before_journey", "current_occupancy_percent", 
        "seat_type", "route_type", "day_of_week", "seats_requested", 
        "is_holiday_season", "booking_hour", "was_confirmed"
    ]
    
    seat_types = ["upper", "middle", "lower"]
    route_types = ["full", "partial"]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    data = []
    for i in range(1, num_records + 1):
        booking_id = f"BK{i:03d}"
        days_before = random.randint(1, 30)
        occupancy = random.randint(20, 95)
        seat_type = random.choice(seat_types)
        route_type = random.choice(route_types)
        day_of_week = random.choice(days_of_week)
        seats_requested = random.randint(1, 6)
        is_holiday = 1 if random.random() < 0.2 else 0
        booking_hour = random.randint(0, 23)
        
        # Confirmation logic based on rules
        high_prob = (
            days_before > 10 and 
            occupancy < 70 and 
            seats_requested <= 2 and 
            seat_type in ["upper", "middle"] and 
            is_holiday == 0
        )
        
        low_prob = (
            days_before < 5 and 
            occupancy > 80 and 
            seats_requested > 3 and 
            seat_type == "lower" and 
            is_holiday == 1
        )
        
        if high_prob:
            was_confirmed = 1 if random.random() < 0.95 else 0
        elif low_prob:
            was_confirmed = 1 if random.random() < 0.2 else 0
        else:
            # Medium probability - weighted factors
            prob = 0.5
            if days_before > 15: prob += 0.2
            if occupancy < 50: prob += 0.15
            if seats_requested == 1: prob += 0.1
            if is_holiday == 1: prob -= 0.25
            if seat_type == "lower": prob -= 0.1
            
            prob = max(0.05, min(0.95, prob))
            was_confirmed = 1 if random.random() < prob else 0
            
        data.append([
            booking_id, days_before, occupancy, seat_type, route_type, 
            day_of_week, seats_requested, is_holiday, booking_hour, was_confirmed
        ])
        
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Generated {num_records} records in {filename}")

if __name__ == "__main__":
    generate_mock_data("app/data/historical_bookings.csv")
