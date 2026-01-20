from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from ...api.dependencies import get_db
from ...services.meal_service import MealService
from ...schemas.seat import Meal, MealCreate

router = APIRouter()


@router.get("/")
async def get_available_meals(db: Session = Depends(get_db)):
    """Get all available meals"""
    meals = MealService.get_available_meals(db)
    return meals


@router.get("/category/{category}")
async def get_meals_by_category(
    category: str = Path(..., description="Meal category (VEG, NON_VEG, DESSERT, BEVERAGE)"),
    db: Session = Depends(get_db)
):
    """Get meals by category"""
    meals = MealService.get_meals_by_category(db, category)
    return meals


@router.get("/{meal_id}")
async def get_meal(meal_id: int, db: Session = Depends(get_db)):
    """Get meal details by ID"""
    meal = MealService.get_meal_by_id(db, meal_id)
    return meal


@router.post("/", response_model=Meal)
async def create_meal(
    meal: MealCreate,
    db: Session = Depends(get_db)
):
    """Create a new meal"""
    new_meal = MealService.create_meal(
        db,
        meal.name,
        meal.description,
        meal.price,
        meal.category
    )
    return new_meal


@router.put("/{meal_id}/availability/{is_available}")
async def update_meal_availability(
    meal_id: int,
    is_available: bool,
    db: Session = Depends(get_db)
):
    """Update meal availability"""
    meal = MealService.update_meal_availability(db, meal_id, is_available)
    return meal
