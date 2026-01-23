# Booking Confirmation Prediction System

## 1. Overview
A **Logistic Regression model** trained on synthetically generated booking data is used to estimate booking confirmation probability. Feature contributions are interpreted qualitatively based on learned coefficient weights to provide explainability without exposing internal model parameters.

## 2. Problem Statement
Given booking parameters (lead time, occupancy, seat preference, route profile, holiday flag, booking time, party size), estimate the likelihood (50–95%) that the booking will be confirmed.

## 3. ML Model (Production)

### 3.1 Model Architecture
- **Algorithm**: Logistic Regression (binary classification)
- **Framework**: scikit-learn
- **Training Data**: 500-1000 synthetic booking records with realistic distributions
- **Target**: Binary confirmed/not-confirmed label

### 3.2 Feature Set
The model uses 8 features in the following order:
1. `days_before_journey` (continuous) - Booking lead time
2. `current_occupancy_percent` (continuous) - Current bus occupancy
3. `seat_type` (categorical → encoded) - Lower/Upper/Middle berth
4. `route_type` (categorical → encoded) - Full/Partial journey
5. `day_of_week` (categorical → encoded) - Day of travel
6. `seats_requested` (discrete) - Number of seats in booking
7. `is_holiday_season` (binary) - Holiday period flag
8. `booking_hour` (discrete) - Hour of booking (0-23)

### 3.3 Model Performance
- **Accuracy**: ~82% on test set
- **Probability Range**: Clamped to 50-95% for business realism
- **Cancellation Risk**: Computed as `(100 - probability) × 0.85`, clamped to 8-25%

### 3.4 Mock Dataset Structure (Synthetic)
The training dataset is synthetically generated to simulate real booking behavior. Each record contains:

- days_before_journey (int)
- current_occupancy_percent (float)
- seat_type (categorical)
- route_type (categorical)
- day_of_week (categorical)
- seats_requested (int)
- is_holiday_season (binary)
- booking_hour (int)
- confirmed (binary target)

Example (synthetic): days_before_journey=3, occupancy=70, seat_type=lower, route_type=partial, holiday=0 → confirmed=1

## 4. Explainability Layer

### 4.1 Coefficient-Based Factor Interpretation
The model exposes feature importance through **qualitative impact descriptions** derived from learned coefficients:

| Coefficient Magnitude | Interpretation |
|-----------------------|----------------|
| |coef| > 0.5 | Strong impact (positive/negative) |
| |coef| > 0.2 | Moderate impact |
| |coef| > 0.05 | Mild impact |
| |coef| ≤ 0.05 | Neutral |

**Example coefficients** (from training):
- `is_holiday_season`: -0.96 → "Strong negative impact"
- `days_before_journey`: +0.42 → "Moderate positive impact"
- `current_occupancy_percent`: -0.28 → "Moderate negative impact"
- `seat_type`: +0.15 → "Mild positive impact"

### 4.2 Factor Response Format
```json
{
  "factors": {
    "lead_time": "Moderate positive impact",
    "occupancy": "Moderate negative impact",
    "seat_preference": "Mild positive impact",
    "holiday_season": "Strong negative impact",
    "route_profile": "Neutral",
    "booking_time": "Neutral",
    "party_size": "Mild positive impact"
  }
}
```

This approach provides **post-hoc interpretability** without exposing exact model parameters.

## 5. Fallback Mechanism
If the trained model is unavailable (missing files), the system falls back to a **rule-based heuristic** that approximates ML behavior:
- Base probability: 80%
- Adjustments based on feature thresholds
- Same output format for API consistency

## 6. API Integration
- Endpoint: `POST /prediction/booking-confirmation`
- The endpoint accepts booking parameters and returns ML-based prediction
- All feature fields have sensible defaults for minimal input

**Request Example:**
```json
{
  "booking_reference": "BUS-AHM-VAP-20260123-P0UK",
  "user_name": "Dhvani",
  "email": "dhvani@email.com",
  "phone": "9XXXXXXXXX",
  "from_station_id": 1,
  "to_station_id": 4,
  "seat_type": "lower",
  "seats_requested": 1,
  "booking_hour": 22,
  "is_holiday_season": false,
  "current_occupancy_percent": 70,
  "days_before_journey": 3
}
```

**Response Example:**
```json
{
  "confirmation_probability": 82.5,
  "cancellation_risk": 14.5,
  "recommendation": "GOOD_CHANCE",
  "factors": {
    "lead_time": "Moderate positive impact",
    "occupancy": "Moderate negative impact",
    "seat_preference": "Mild positive impact",
    "holiday_season": "Neutral",
    "route_profile": "Neutral",
    "booking_time": "Neutral",
    "party_size": "Mild positive impact"
  }
}
```

## 7. Key Design Decisions

### 7.1 Why Logistic Regression?
- **Interpretable**: Coefficients directly map to feature importance
- **Fast**: Sub-millisecond prediction latency
- **Proven**: Industry standard for probability estimation
- **Explainable**: Supports regulatory and business requirements

### 7.2 Why Qualitative Factors?
- Protects model internals (coefficients not exposed)
- User-friendly for non-technical stakeholders
- Consistent with industry best practices for ML explainability

### 7.3 Why 50-95% Range?
- Avoids overconfidence (no 100% guarantees)
- Realistic for sleeper bus booking scenarios
- Allows for system uncertainties and edge cases
