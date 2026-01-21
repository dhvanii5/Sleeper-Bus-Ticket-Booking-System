from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...api.dependencies import get_db
from ...models.meal import Meal
from ...schemas.schemas import Meal as MealSchema

router = APIRouter()

@router.get("/", response_model=List[MealSchema])
async def get_meals(db: Session = Depends(get_db)):
    """
    Get list of available meals
    """
    meals = db.query(Meal).filter(Meal.is_available == True).all()
    return meals
