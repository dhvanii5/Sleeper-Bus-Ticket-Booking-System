"""
Heuristic prediction service for booking confirmation probability.

This module delivers the “ML-like” scoring requested in the assignment using a
transparent rule-based heuristic. It is intentionally explainable: each feature
contributes a percentage delta that rolls up into the final score and is
returned as part of the response for UI surfacing.

See PREDICTION_APPROACH.md for the documented rationale.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class PredictionResult:
    confirmation_probability: float
    cancellation_risk: float
    recommendation: str
    factors: Dict[str, str]


class PredictionService:
    BASE_PROBABILITY = 80.0
    MIN_PROBABILITY = 50.0
    MAX_PROBABILITY = 95.0

    @staticmethod
    def predict(request_data: dict) -> PredictionResult:
        """
        Apply heuristic weights to estimate confirmation probability.
        The factor strings (e.g., "+5%") are returned to keep the API
        explainable for product/QA reviewers.
        """

        probability = PredictionService.BASE_PROBABILITY
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
        else:
            factors["holiday_season"] = "0%"

        # Route profile (full vs partial journey)
        route_type = request_data.get("route_type", "full")
        if route_type == "full":
            probability += 2
            factors["route_profile"] = "+2%"
        else:
            factors["route_profile"] = "0%"

        # Booking time (late night gets slight boost)
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
        probability = max(PredictionService.MIN_PROBABILITY,
                          min(PredictionService.MAX_PROBABILITY, probability))

        # Cancellation risk - realistic range (8-25%)
        # Higher when probability is lower
        base_risk = 100 - probability
        cancellation_risk = round(base_risk * 0.85, 2)
        cancellation_risk = max(8.0, min(25.0, cancellation_risk))

        # Recommendation buckets
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
            "current_occupancy_percent": 50,  # Default assumption
            "seat_type": "lower",
            "is_holiday_season": False,
            "route_type": "full",
            "booking_hour": datetime.now().hour
        }
        
        result = PredictionService.predict(request_data)
        return result.confirmation_probability
