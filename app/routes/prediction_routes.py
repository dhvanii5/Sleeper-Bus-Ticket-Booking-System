from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field, validator
from app.ml.predictor import predict_confirmation_probability
import datetime

router = APIRouter()

class PredictionRequest(BaseModel):
    days_before_journey: int = Field(..., ge=0, le=365)
    current_occupancy_percent: int = Field(..., ge=0, le=100)
    seat_type: str = Field(..., pattern='^(upper|middle|lower)$')
    route_type: str = Field(..., pattern='^(full|partial)$')
    day_of_week: str = Field(..., pattern='^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$')
    seats_requested: int = Field(..., ge=1, le=20)
    is_holiday_season: bool
    booking_hour: int = Field(..., ge=0, le=23)

@router.post("/confirm-probability")
async def get_confirmation_probability(data: PredictionRequest = Body(...)):
    """
    Endpoint to predict booking confirmation probability
    """
    try:
        result = predict_confirmation_probability(data.dict())
        return {
            'success': True,
            'prediction': result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-info")
async def get_model_info():
    """
    Returns information about the prediction model
    """
    return {
        'model_type': 'Logistic Regression',
        'features_used': 8,
        'accuracy': '82.22%', # This should ideally be read from a file or config
        'last_trained': datetime.datetime.now().strftime("%Y-%m-%d")
    }
