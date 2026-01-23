from fastapi import APIRouter
from ...services.prediction_service import PredictionService
from ...schemas.schemas import PredictionRequest, PredictionResponse

router = APIRouter()


@router.post("/booking-confirmation", response_model=PredictionResponse)
async def predict_booking_confirmation(prediction_request: PredictionRequest):
    """Single heuristic endpoint for confirmation probability."""
    result = PredictionService.predict(prediction_request.dict())

    return PredictionResponse(
        confirmation_probability=result.confirmation_probability,
        cancellation_risk=result.cancellation_risk,
        recommendation=result.recommendation,
        factors=result.factors,
    )
