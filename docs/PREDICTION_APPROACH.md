# Booking Confirmation Prediction System

## 1. Overview
This document describes the machine learning system that predicts the probability of booking confirmation for the Ahmedabad-Mumbai sleeper bus service.

## 2. Problem Statement
Given booking parameters (timing, seat preferences, route details), predict the likelihood (0-100%) that the booking will be confirmed based on historical patterns.

## 3. Dataset

### 3.1 Data Source
Mock historical booking data containing 450 records from past 6 months.

### 3.2 Dataset Structure
- **Total Records:** 450
- **Confirmed Bookings:** ~70%
- **Cancelled/Not Confirmed:** ~30%

**Features (8 total):**
1. `days_before_journey`: Days between booking and journey (1-30)
2. `current_occupancy_percent`: Bus occupancy at booking time (0-100)
3. `seat_type`: upper/middle/lower
4. `route_type`: full/partial journey
5. `day_of_week`: Monday to Sunday
6. `seats_requested`: Number of seats (1-6)
7. `is_holiday_season`: Boolean flag
8. `booking_hour`: Hour of day (0-23)

**Target Variable:**
- `was_confirmed`: 1 (confirmed) or 0 (not confirmed)

## 4. Feature Engineering

### 4.1 Categorical Encoding
- **seat_type**: Label encoding
- **route_type**: Label encoding
- **day_of_week**: Label encoding

### 4.2 Feature Importance Analysis
Based on model coefficients:
- `is_holiday_season`: -0.96 (Strong negative impact)
- `route_type_encoded`: -0.37
- `seats_requested`: -0.15
- `days_before_journey`: +0.42 (Strong positive impact - from training logs)

## 5. Model Selection

### 5.1 Chosen Model: Logistic Regression
**Rationale:**
- Direct probability output (0-100%)
- Interpretable coefficients
- Fast training and prediction
- industry standard for binary classification

## 6. Training Methodology
- Training: 80% (360 records)
- Testing: 20% (90 records)
- Stratified split to maintain class balance

## 7. Model Evaluation
- **Accuracy**: 82.22% (approx)
- **Precision/Recall/F1**: High for confirmed class.

## 8. Prediction Output

### 8.1 Probability Calculation
Model outputs probability using sigmoid function.

### 8.2 Confidence Levels
- 90-100%: Very High
- 75-89%: High
- 50-74%: Moderate
- 30-49%: Low
- 0-29%: Very Low

## 9. API Integration

### 9.1 Endpoint
`POST /api/prediction/confirm-probability`

### 9.2 Request Format
```json
{
  "days_before_journey": 10,
  "current_occupancy_percent": 62,
  "seat_type": "upper",
  "route_type": "full",
  "day_of_week": "Friday",
  "seats_requested": 2,
  "is_holiday_season": false,
  "booking_hour": 14
}
```

## 10. Deployment
- Model: `app/ml/saved_models/booking_predictor.pkl`
- Encoders: `app/ml/saved_models/encoders.pkl`
