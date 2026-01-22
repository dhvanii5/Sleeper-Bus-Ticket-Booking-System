import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Load saved model and encoders at module level
MODEL_DIR = Path('app/ml/saved_models')
MODEL_PATH = MODEL_DIR / 'booking_predictor.pkl'
ENCODER_PATH = MODEL_DIR / 'encoders.pkl'

_model = None
_encoders = None

def _load_model_assets():
    global _model, _encoders
    if _model is None or _encoders is None:
        if not MODEL_PATH.exists() or not ENCODER_PATH.exists():
            raise FileNotFoundError("Model or encoders not found. Please run training script first.")
        _model = joblib.load(MODEL_PATH)
        _encoders = joblib.load(ENCODER_PATH)

def get_confidence_level(percentage):
    if percentage >= 90: return "Very High"
    if percentage >= 75: return "High"
    if percentage >= 50: return "Moderate"
    if percentage >= 30: return "Low"
    return "Very Low"

def analyze_factors(booking_data, probability):
    positive_factors = []
    negative_factors = []
    
    # Check days_before_journey
    days = booking_data['days_before_journey']
    if days > 15:
        positive_factors.append(f"Booking {days} days in advance (+15%)")
    elif days > 10:
        positive_factors.append(f"Booking {days} days in advance (+10%)")
    elif days < 5:
        negative_factors.append(f"Late booking ({days} days) (-10%)")

    # Check occupancy
    occ = booking_data['current_occupancy_percent']
    if occ < 50:
        positive_factors.append("Very low current occupancy (+15%)")
    elif occ < 70:
        positive_factors.append("Moderate occupancy (+5%)")
    elif occ > 85:
        negative_factors.append("High occupancy (-15%)")

    # Check seat_type
    seat = booking_data['seat_type']
    if seat == 'upper':
        positive_factors.append("Upper berth selected (+8%)")
    elif seat == 'lower':
        negative_factors.append("Lower berth requested (-5%)")

    # Check holiday
    if booking_data['is_holiday_season']:
        negative_factors.append("Holiday season rush (-12%)")
    else:
        positive_factors.append("Non-holiday period (+5%)")

    # Check seats requested
    if booking_data['seats_requested'] == 1:
        positive_factors.append("Individual seat booking (+5%)")
    elif booking_data['seats_requested'] > 3:
        negative_factors.append(f"Large group ({booking_data['seats_requested']} seats) (-8%)")

    return positive_factors, negative_factors

def predict_confirmation_probability(booking_data):
    """
    Input: dictionary with booking details
    Output: dictionary with probability and metadata
    """
    _load_model_assets()
    
    # Extract features and encode
    try:
        seat_encoded = _encoders['seat_type'].transform([booking_data['seat_type']])[0]
        route_encoded = _encoders['route_type'].transform([booking_data['route_type']])[0]
        day_encoded = _encoders['day_of_week'].transform([booking_data['day_of_week']])[0]
    except ValueError as e:
        raise ValueError(f"Invalid categorical value: {str(e)}")

    # Feature order must match training
    # [days_before_journey, current_occupancy_percent, seat_type_encoded, 
    #  route_type_encoded, day_of_week_encoded, seats_requested, 
    #  is_holiday_season, booking_hour]
    features = [
        booking_data['days_before_journey'],
        booking_data['current_occupancy_percent'],
        seat_encoded,
        route_encoded,
        day_encoded,
        booking_data['seats_requested'],
        1 if booking_data['is_holiday_season'] else 0,
        booking_data['booking_hour']
    ]
    
    # Get probability of class 1
    prob = _model.predict_proba([features])[0][1]
    percentage = round(prob * 100, 2)
    
    confidence_level = get_confidence_level(percentage)
    
    # Recommendation
    if percentage >= 75:
        recommendation = "Good chance of confirmation. Proceed with booking."
    elif percentage >= 50:
        recommendation = "Moderate chance. You may want to consider alternative timings if possible."
    else:
        recommendation = "Low chance of confirmation. High risk of remaining waitlisted."

    pos_factors, neg_factors = analyze_factors(booking_data, percentage)
    
    return {
        'confirmation_probability': percentage,
        'confidence_level': confidence_level,
        'recommendation': recommendation,
        'factors': {
            'positive': pos_factors,
            'negative': neg_factors
        }
    }
