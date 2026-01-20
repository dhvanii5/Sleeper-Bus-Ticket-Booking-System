from sqlalchemy.orm import Session
from ..models.meal import Meal
from ..core.exceptions import InvalidBookingException


class MealService:
    """Service to handle meal management"""
    
    @staticmethod
    def get_available_meals(db: Session) -> list:
        """Get all available meals"""
        meals = db.query(Meal).filter(Meal.is_available == True).all()
        return meals
    
    @staticmethod
    def get_meal_by_id(db: Session, meal_id: int) -> Meal:
        """Get meal details by ID"""
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise InvalidBookingException("Meal not found")
        return meal
    
    @staticmethod
    def get_meals_by_category(db: Session, category: str) -> list:
        """Get meals by category"""
        meals = db.query(Meal).filter(
            Meal.category == category,
            Meal.is_available == True
        ).all()
        return meals
    
    @staticmethod
    def create_meal(
        db: Session,
        name: str,
        description: str,
        price: int,
        category: str
    ) -> Meal:
        """Create a new meal"""
        meal = Meal(
            name=name,
            description=description,
            price=price,
            category=category,
            is_available=True
        )
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
    
    @staticmethod
    def update_meal_availability(
        db: Session,
        meal_id: int,
        is_available: bool
    ) -> Meal:
        """Update meal availability"""
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise InvalidBookingException("Meal not found")
        
        meal.is_available = is_available
        db.commit()
        db.refresh(meal)
        return meal
