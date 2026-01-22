from app.ml.predictor import predict_confirmation_probability
import json

def test_predictor():
    high_prob_data = {
        "days_before_journey": 25,
        "current_occupancy_percent": 35,
        "seat_type": "upper",
        "route_type": "full",
        "day_of_week": "Tuesday",
        "seats_requested": 1,
        "is_holiday_season": False,
        "booking_hour": 10
    }
    
    low_prob_data = {
        "days_before_journey": 2,
        "current_occupancy_percent": 90,
        "seat_type": "lower",
        "route_type": "partial",
        "day_of_week": "Saturday",
        "seats_requested": 4,
        "is_holiday_season": True,
        "booking_hour": 22
    }
    
    print("Testing High Probability Scenario:")
    result_high = predict_confirmation_probability(high_prob_data)
    print(json.dumps(result_high, indent=2))
    
    print("\nTesting Low Probability Scenario:")
    result_low = predict_confirmation_probability(low_prob_data)
    print(json.dumps(result_low, indent=2))

if __name__ == "__main__":
    test_predictor()
