import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def train_model():
    # 1. Load dataset
    data_path = 'app/data/historical_bookings.csv'
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Dataset loaded: {len(df)} records")

    # 2. Preprocessing & Encoding
    print("Preprocessing data...")
    
    # Encoders dictionary to save
    encoders = {}
    
    # seat_type: upper/middle/lower → 2/1/0 (Manually mapping for consistency if needed, 
    # but LabelEncoder is fine as long as we save it)
    seat_encoder = LabelEncoder()
    df['seat_type_encoded'] = seat_encoder.fit_transform(df['seat_type'])
    encoders['seat_type'] = seat_encoder
    
    # route_type: full/partial
    route_encoder = LabelEncoder()
    df['route_type_encoded'] = route_encoder.fit_transform(df['route_type'])
    encoders['route_type'] = route_encoder
    
    # day_of_week
    day_encoder = LabelEncoder()
    df['day_of_week_encoded'] = day_encoder.fit_transform(df['day_of_week'])
    encoders['day_of_week'] = day_encoder

    # 3. Prepare feature matrix X and target y
    # Feature order: [days_before_journey, current_occupancy_percent, seat_type_encoded, 
    #                route_type_encoded, day_of_week_encoded, seats_requested, 
    #                is_holiday_season, booking_hour]
    features = [
        'days_before_journey', 'current_occupancy_percent', 'seat_type_encoded',
        'route_type_encoded', 'day_of_week_encoded', 'seats_requested',
        'is_holiday_season', 'booking_hour'
    ]
    X = df[features]
    y = df['was_confirmed']

    # 4. Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} records")
    print(f"Test set: {len(X_test)} records")

    # 5. Train Logistic Regression
    print("\nModel Training...")
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    print("Training completed!")

    # 6. Evaluate model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"\nEvaluation Metrics:")
    print(f"Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    # 7. Save model and encoders
    model_dir = 'app/ml/saved_models'
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'booking_predictor.pkl')
    encoder_path = os.path.join(model_dir, 'encoders.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(encoders, encoder_path)
    print(f"\nModel saved successfully to {model_path}!")
    print(f"Encoders saved successfully to {encoder_path}!")

    # 8. Feature Importance
    print("\nFeature Importance (Coefficients):")
    coefficients = pd.DataFrame({
        'Feature': features,
        'Coefficient': model.coef_[0]
    }).sort_values(by='Coefficient', ascending=False)
    print(coefficients)

if __name__ == "__main__":
    train_model()
