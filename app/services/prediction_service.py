"""
ML-based prediction service for booking confirmation probability.

A Logistic Regression model trained on synthetically generated booking data 
is used to estimate booking confirmation probability. Feature contributions 
are interpreted qualitatively based on learned coefficient weights to provide 
explainability without exposing internal model parameters.
"""

from dataclasses import dataclass
from typing import Dict
from pathlib import Path


@dataclass
class PredictionResult:
    confirmation_probability: float
    cancellation_risk: float
    recommendation: str
    factors: Dict[str, str]


class PredictionService:
    _model = None
    _encoders = None
    _coefficients = None
    
    @staticmethod
    def _load_model():
        """Lazy load the trained model and encoders"""
        if PredictionService._model is None:
            try:
                import joblib
                MODEL_DIR = Path('app/ml/saved_models')
                MODEL_PATH = MODEL_DIR / 'booking_predictor.pkl'
                ENCODER_PATH = MODEL_DIR / 'encoders.pkl'
                
                if not MODEL_PATH.exists() or not ENCODER_PATH.exists():
                    # Fallback to heuristic if model not found
                    return False
                    
                PredictionService._model = joblib.load(MODEL_PATH)
                PredictionService._encoders = joblib.load(ENCODER_PATH)
                
                # Extract coefficients for explanations
                # Feature order: [days_before_journey, current_occupancy_percent, seat_type_encoded,
                #                route_type_encoded, day_of_week_encoded, seats_requested,
                #                is_holiday_season, booking_hour]
                PredictionService._coefficients = {
                    'days_before_journey': PredictionService._model.coef_[0][0],
                    'current_occupancy_percent': PredictionService._model.coef_[0][1],
                    'seat_type': PredictionService._model.coef_[0][2],
                    'route_type': PredictionService._model.coef_[0][3],
                    'day_of_week': PredictionService._model.coef_[0][4],
                    'seats_requested': PredictionService._model.coef_[0][5],
                    'is_holiday_season': PredictionService._model.coef_[0][6],
                    'booking_hour': PredictionService._model.coef_[0][7]
                }
                return True
            except Exception as e:
                print(f"Failed to load model: {e}")
                return False
        return True
    
    @staticmethod
    def _explain_coefficient(coef: float) -> str:
        """Convert coefficient to qualitative impact description"""
        if abs(coef) > 0.5:
            return "Strong positive impact" if coef > 0 else "Strong negative impact"
        elif abs(coef) > 0.2:
            return "Moderate positive impact" if coef > 0 else "Moderate negative impact"
        elif abs(coef) > 0.05:
            return "Mild positive impact" if coef > 0 else "Mild negative impact"
        else:
            return "Neutral"
    
    @staticmethod
    def predict(request_data: dict) -> PredictionResult:
        """
        Apply ML model to estimate confirmation probability.
        Falls back to heuristic if model is not available.
        """
        # Try to use ML model
        if PredictionService._load_model():
            try:
                return PredictionService._predict_ml(request_data)
            except Exception as e:
                print(f"ML prediction failed: {e}, falling back to heuristic")
        
        # Fallback to heuristic
        return PredictionService._predict_heuristic(request_data)
    
    @staticmethod
    def _predict_ml(request_data: dict) -> PredictionResult:
        """ML-based prediction using trained logistic regression model"""
        # Encode categorical features
        seat_type = request_data.get('seat_type', 'lower')
        route_type = request_data.get('route_type', 'full')
        day_of_week = request_data.get('day_of_week', 'Monday')
        
        try:
            seat_encoded = PredictionService._encoders['seat_type'].transform([seat_type])[0]
            route_encoded = PredictionService._encoders['route_type'].transform([route_type])[0]
            day_encoded = PredictionService._encoders['day_of_week'].transform([day_of_week])[0]
        except:
            # If encoding fails, use defaults
            seat_encoded = 0
            route_encoded = 0
            day_encoded = 0
        
        # Prepare features in exact order
        features = [
            request_data.get('days_before_journey', 7),
            request_data.get('current_occupancy_percent', 50),
            seat_encoded,
            route_encoded,
            day_encoded,
            request_data.get('seats_requested', 1),
            1 if request_data.get('is_holiday_season', False) else 0,
            request_data.get('booking_hour', 12)
        ]
        
        # Get probability from model
        prob = PredictionService._model.predict_proba([features])[0][1]
        probability = round(min(prob * 100, 95), 2)
        
        # Build factor explanations based on coefficients
        factors = {
            "lead_time": PredictionService._explain_coefficient(
                PredictionService._coefficients['days_before_journey']
            ),
            "occupancy": PredictionService._explain_coefficient(
                PredictionService._coefficients['current_occupancy_percent']
            ),
            "seat_preference": PredictionService._explain_coefficient(
                PredictionService._coefficients['seat_type']
            ),
            "holiday_season": PredictionService._explain_coefficient(
                PredictionService._coefficients['is_holiday_season']
            ),
            "route_profile": PredictionService._explain_coefficient(
                PredictionService._coefficients['route_type']
            ),
            "booking_time": PredictionService._explain_coefficient(
                PredictionService._coefficients['booking_hour']
            ),
            "party_size": PredictionService._explain_coefficient(
                PredictionService._coefficients['seats_requested']
            )
        }
        
        # Realistic cancellation risk (8-25% range)
        base_risk = 100 - probability
        cancellation_risk = round(base_risk * 0.85, 2)
        cancellation_risk = max(8.0, min(25.0, cancellation_risk))
        
        # Recommendation
        if probability >= 85:
            recommendation = "HIGH_CHANCE"
        elif probability >= 70:
            recommendation = "GOOD_CHANCE"
        elif probability >= 60:
            recommendation = "REVIEW_SUGGESTED"
        else:
            recommendation = "MONITOR_CLOSELY"
        
        return PredictionResult(
            confirmation_probability=probability,
            cancellation_risk=cancellation_risk,
            recommendation=recommendation,
            factors=factors
        )
    
    @staticmethod
    def _predict_heuristic(request_data: dict) -> PredictionResult:
        """Fallback heuristic-based prediction when ML model is unavailable"""
        BASE_PROBABILITY = 80.0
        MIN_PROBABILITY = 50.0
        MAX_PROBABILITY = 95.0
        
        probability = BASE_PROBABILITY
        factors = {
            "lead_time": "0%",
            "occupancy": "0%",
            "seat_preference": "0%",
            "holiday_season": "0%",
            "route_profile": "0%",
            "booking_time": "0%",
            "party_size": "0%",
        }

        # Lead time
        days = request_data.get("days_before_journey", 0)
        if days == 0:
            probability -= 10
            factors["lead_time"] = "-10%"
        elif days >= 14:
            probability += 8
            factors["lead_time"] = "+8%"
        elif days >= 7:
            probability += 6
            factors["lead_time"] = "+6%"
        elif days >= 3:
            probability += 5
            factors["lead_time"] = "+5%"
        elif days == 1:
            probability -= 5
            factors["lead_time"] = "-5%"

        # Occupancy impact
        occupancy = request_data.get("current_occupancy_percent", 0)
        if occupancy >= 80:
            probability -= 15
            factors["occupancy"] = "-15%"
        elif occupancy >= 60:
            probability -= 5
            factors["occupancy"] = "-5%"
        elif occupancy < 40:
            probability += 5
            factors["occupancy"] = "+5%"

        # Seat preference
        seat_type = request_data.get("seat_type", "lower")
        if seat_type == "lower":
            probability += 5
            factors["seat_preference"] = "+5%"
        elif seat_type == "upper":
            probability += 3
            factors["seat_preference"] = "+3%"

        # Holiday season
        if request_data.get("is_holiday_season", False):
            probability -= 10
            factors["holiday_season"] = "-10%"

        # Route profile
        route_type = request_data.get("route_type", "full")
        if route_type == "full":
            probability += 2
            factors["route_profile"] = "+2%"

        # Booking time
        hour = request_data.get("booking_hour", 12)
        if hour >= 21 or hour <= 5:
            probability += 2
            factors["booking_time"] = "+2%"

        # Party size
        seats_requested = request_data.get("seats_requested", 1)
        if seats_requested > 2:
            probability -= 5
            factors["party_size"] = "-5%"
        else:
            probability += 1
            factors["party_size"] = "+1%"

        # Clamp range
        probability = max(MIN_PROBABILITY, min(MAX_PROBABILITY, probability))

        # Cancellation risk
        base_risk = 100 - probability
        cancellation_risk = round(base_risk * 0.85, 2)
        cancellation_risk = max(8.0, min(25.0, cancellation_risk))

        # Recommendation
        if probability >= 85:
            recommendation = "HIGH_CHANCE"
        elif probability >= 70:
            recommendation = "GOOD_CHANCE"
        elif probability >= 60:
            recommendation = "REVIEW_SUGGESTED"
        else:
            recommendation = "MONITOR_CLOSELY"

        return PredictionResult(
            confirmation_probability=round(probability, 2),
            cancellation_risk=cancellation_risk,
            recommendation=recommendation,
            factors=factors,
        )

    @staticmethod
    def predict_confirmation_probability(
        booking_date,
        journey_date,
        num_seats: int = 1
    ) -> float:
        """
        Simplified prediction method for booking creation.
        Returns just the confirmation probability as a float.
        
        Args:
            booking_date: Date when booking is being made
            journey_date: Date of travel
            num_seats: Number of seats being booked
            
        Returns:
            Confirmation probability as a percentage (0-100)
        """
        from datetime import datetime
        
        # Calculate days before journey
        if isinstance(booking_date, str):
            booking_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        if isinstance(journey_date, str):
            journey_date = datetime.strptime(journey_date, "%Y-%m-%d").date()
            
        days_before = (journey_date - booking_date).days
        
        # Build minimal request data for the main predict method
        request_data = {
            "days_before_journey": days_before,
            "seats_requested": num_seats,
            "current_occupancy_percent": 50,
            "seat_type": "lower",
            "is_holiday_season": False,
            "route_type": "full",
            "booking_hour": datetime.now().hour,
            "day_of_week": datetime.now().strftime('%A')
        }
        
        result = PredictionService.predict(request_data)
        return result.confirmation_probability
