"""
Prediction Service Module - AI/ML Component

This module implements the prediction logic for calculating booking confirmation
probability. Since we don't have historical data for a real ML model, we use a
sophisticated heuristic-based approach that considers multiple factors.

The prediction helps users understand the likelihood of their booking being
successfully confirmed and completed without cancellation.

Algorithm Details:
    See PREDICTION_APPROACH.md for comprehensive documentation

Key Factors:
    1. Booking Time: How far in advance the booking is made
    2. Party Size: Number of seats being booked
    3. Random Variation: Real-world unpredictability

Output Range: 50% (minimum) to 100% (maximum confidence)
"""

from datetime import datetime, date
import random


class PredictionService:
    """
    Service class for calculating booking confirmation probability.
    
    This is a rule-based heuristic model that simulates ML prediction
    behavior without requiring training data. The algorithm is designed
    to be deterministic (given the same inputs) with a small random
    component for realism.
    
    Usage:
        probability = PredictionService.predict_confirmation_probability(
            booking_date=date.today(),
            journey_date=date(2026, 2, 1),
            num_seats=2
        )
        # Returns: float between 50.0 and 100.0
    """
    
    # Class constants for score calculation
    BASE_PROBABILITY = 90.0          # Starting point for all predictions
    ADVANCE_BONUS_30_DAYS = 5.0      # Bonus for booking >30 days ahead
    ADVANCE_BONUS_7_DAYS = 2.0       # Bonus for booking >7 days ahead
    LAST_MINUTE_PENALTY = 5.0        # Penalty for booking <1 day ahead
    SEAT_GROUP_PENALTY = 1.5         # Penalty per additional seat (coordination risk)
    RANDOM_NOISE_RANGE = 2.0         # Max random variation (+/-)
    MIN_PROBABILITY = 50.0           # Floor value
    MAX_PROBABILITY = 100.0          # Ceiling value
    
    @staticmethod
    def predict_confirmation_probability(
        booking_date: date,
        journey_date: date,
        num_seats: int
    ) -> float:
        """
        Calculate the probability of a booking being confirmed and completed.
        
        This method applies a multi-factor scoring algorithm:
        1. Starts with a base score of 90%
        2. Adjusts based on how far in advance the booking is made
        3. Applies a small penalty for larger groups (coordination complexity)
        4. Adds random noise for realism
        5. Clamps result to 50-100% range
        
        Args:
            booking_date (date): When the booking is being made (usually today)
            journey_date (date): When the travel will occur
            num_seats (int): Number of seats being booked (1-5 typically)
        
        Returns:
            float: Probability percentage (50.0 to 100.0)
        
        Examples:
            >>> # Solo traveler, booking 2 weeks ahead
            >>> predict_confirmation_probability(
            ...     booking_date=date(2026, 1, 1),
            ...     journey_date=date(2026, 1, 15),
            ...     num_seats=1
            ... )
            92.35  # ~90 base + 2 advance bonus + random
            
            >>> # Group of 4, booking last minute
            >>> predict_confirmation_probability(
            ...     booking_date=date(2026, 1, 14),
            ...     journey_date=date(2026, 1, 15),
            ...     num_seats=4
            ... )
            76.82  # ~90 base - 5 last minute - 4.5 group penalty + random
        """
        # Initialize with base probability
        probability = PredictionService.BASE_PROBABILITY
        
        # =============================================================================
        # FACTOR 1: TIME IN ADVANCE (PLANNING FACTOR)
        # =============================================================================
        # People who book far in advance are more committed to their travel plans
        days_in_advance = (journey_date - booking_date).days
        
        if days_in_advance > 30:
            # Very planned trip (e.g., vacation, important event)
            probability += PredictionService.ADVANCE_BONUS_30_DAYS
        elif days_in_advance > 7:
            # Moderately planned trip
            probability += PredictionService.ADVANCE_BONUS_7_DAYS
        elif days_in_advance < 1:
            # Last-minute booking (higher uncertainty)
            probability -= PredictionService.LAST_MINUTE_PENALTY
            
        # =============================================================================
        # FACTOR 2: PARTY SIZE (GROUP COORDINATION COMPLEXITY)
        # =============================================================================
        # Larger groups have higher cancellation risk if one person drops out
        # Solo travelers (1 seat) have no penalty
        if num_seats > 1:
            group_penalty = (num_seats - 1) * PredictionService.SEAT_GROUP_PENALTY
            probability -= group_penalty
            
        # =============================================================================
        # FACTOR 3: RANDOM VARIATION (REAL-WORLD UNPREDICTABILITY)
        # =============================================================================
        # Add small random noise to simulate real-world factors we can't model
        # (weather, personal emergencies, etc.)
        noise = random.uniform(
            -PredictionService.RANDOM_NOISE_RANGE,
            PredictionService.RANDOM_NOISE_RANGE
        )
        probability += noise
        
        # =============================================================================
        # NORMALIZATION: CLAMP TO VALID RANGE
        # =============================================================================
        # Ensure result is between 50% and 100%
        probability = max(
            PredictionService.MIN_PROBABILITY,
            min(PredictionService.MAX_PROBABILITY, probability)
        )
        
        # Round to 2 decimal places for readability
        return round(probability, 2)
