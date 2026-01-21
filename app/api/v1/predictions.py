from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...api.dependencies import get_db
from ...services.prediction_service import PredictionService
from ...schemas.schemas import PredictionRequest, PredictionResponse

router = APIRouter()


@router.post("/booking-confirmation", response_model=PredictionResponse)
async def predict_booking_confirmation(
    prediction_request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Get booking confirmation probability using ML predictions
    
    Body:
    - booking_reference: Booking reference number
    - user_name: Passenger name
    - email: Passenger email
    - phone: Passenger phone
    - from_station_id: Starting station ID
    - to_station_id: Destination station ID
    
    Returns:
    - confirmation_probability: Likelihood of booking confirmation (0-1)
    - cancellation_risk: Risk of cancellation (0-1)
    - no_show_risk: Risk of no-show (0-1)
    - recommendation: SAFE_TO_CONFIRM, REVIEW_NEEDED, or MONITOR_CLOSELY
    """
    booking_data = prediction_request.dict()
    prediction = PredictionService.predict_booking_confirmation(booking_data)
    return prediction
