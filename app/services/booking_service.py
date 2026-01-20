from sqlalchemy.orm import Session
from datetime import datetime
from ..models.booking import Booking, BookingMeal
from ..models.seat import Seat
from ..models.station import Station
from ..models.meal import Meal
from ..core.exceptions import (
    BookingNotFoundException,
    InvalidStationException,
    CancellationNotAllowedException,
    InvalidBookingException
)
from ..core.security import generate_booking_reference
from ..utils.validators import (
    validate_email,
    validate_phone,
    validate_station_combination
)
from ..utils.helpers import calculate_refund_amount
from .seat_service import SeatService


class BookingService:
    """Service to handle booking logic"""
    
    @staticmethod
    def create_booking(
        db: Session,
        user_name: str,
        email: str,
        phone: str,
        from_station_id: int,
        to_station_id: int,
        seat_id: int,
        journey_date: str,
        meal_ids: list = None
    ) -> Booking:
        """
        Create a new booking with validation
        """
        # Validate input
        if not validate_email(email):
            raise InvalidBookingException("Invalid email format")
        
        if not validate_phone(phone):
            raise InvalidBookingException("Invalid phone number format")
        
        # Get stations
        from_station = db.query(Station).filter(Station.id == from_station_id).first()
        to_station = db.query(Station).filter(Station.id == to_station_id).first()
        
        if not from_station or not to_station:
            raise InvalidStationException("One or both stations not found")
        
        # Validate station combination
        if not validate_station_combination(from_station.sequence, to_station.sequence):
            raise InvalidStationException(
                "From station must come before to station in the route"
            )
        
        # Check seat availability
        SeatService.check_seat_availability(
            db, seat_id, from_station_id, to_station_id, journey_date
        )
        
        # Calculate price
        price = SeatService.calculate_seat_price(
            db, seat_id, from_station_id, to_station_id
        )
        
        # Generate booking reference
        booking_reference = generate_booking_reference(
            from_station.name, to_station.name
        )
        
        # Create booking
        booking = Booking(
            booking_reference=booking_reference,
            user_name=user_name,
            email=email,
            phone=phone,
            from_station_id=from_station_id,
            to_station_id=to_station_id,
            seat_id=seat_id,
            booking_date=datetime.now().strftime("%Y-%m-%d"),
            journey_date=journey_date,
            status="CONFIRMED",
            total_amount=price
        )
        
        db.add(booking)
        db.flush()  # Get booking ID without committing
        
        # Block the seat
        SeatService.block_seat(
            db, seat_id, from_station_id, to_station_id, journey_date, booking.id
        )
        
        # Add meals if provided
        if meal_ids:
            for meal_id in meal_ids:
                meal = db.query(Meal).filter(Meal.id == meal_id).first()
                if meal:
                    booking_meal = BookingMeal(
                        booking_id=booking.id,
                        meal_id=meal_id
                    )
                    db.add(booking_meal)
                    booking.total_amount += meal.price
        
        db.commit()
        db.refresh(booking)
        
        return booking
    
    @staticmethod
    def get_booking_details(db: Session, booking_reference: str) -> Booking:
        """Get booking details by reference"""
        booking = db.query(Booking).filter(
            Booking.booking_reference == booking_reference
        ).first()
        
        if not booking:
            raise BookingNotFoundException("Booking not found")
        
        return booking
    
    @staticmethod
    def get_booking_history(db: Session, email: str) -> list:
        """Get all bookings for a user"""
        bookings = db.query(Booking).filter(Booking.email == email).all()
        return bookings
    
    @staticmethod
    def cancel_booking(db: Session, booking_reference: str) -> dict:
        """
        Cancel a booking with refund calculation
        """
        booking = db.query(Booking).filter(
            Booking.booking_reference == booking_reference
        ).first()
        
        if not booking:
            raise BookingNotFoundException("Booking not found")
        
        if booking.status == "CANCELLED":
            raise InvalidBookingException("Booking is already cancelled")
        
        # Parse journey date
        journey_datetime = datetime.strptime(
            booking.journey_date, "%Y-%m-%d"
        )
        
        # Calculate refund
        refund_info = calculate_refund_amount(
            booking.total_amount,
            journey_datetime,
            datetime.now()
        )
        
        if refund_info["status"] == "NO_REFUND" and refund_info["hours_before_journey"] < 0:
            raise CancellationNotAllowedException(
                "Journey has already started"
            )
        
        # Update booking
        booking.status = "CANCELLED"
        booking.refund_amount = refund_info["refund_amount"]
        booking.cancelled_at = datetime.utcnow()
        
        # Release the seat
        SeatService.release_seat(
            db, booking.seat_id, booking.from_station_id,
            booking.to_station_id, booking.journey_date
        )
        
        db.commit()
        
        return {
            "booking_reference": booking.booking_reference,
            "refund_amount": refund_info["refund_amount"],
            "refund_percentage": refund_info["refund_percentage"],
            "refund_status": refund_info["status"]
        }
    
    @staticmethod
    def update_booking_meals(
        db: Session,
        booking_reference: str,
        meal_ids: list
    ) -> Booking:
        """Update meals for an existing booking"""
        booking = db.query(Booking).filter(
            Booking.booking_reference == booking_reference
        ).first()
        
        if not booking:
            raise BookingNotFoundException("Booking not found")
        
        if booking.status == "CANCELLED":
            raise InvalidBookingException("Cannot update a cancelled booking")
        
        # Remove old meals
        old_meals = db.query(BookingMeal).filter(
            BookingMeal.booking_id == booking.id
        ).all()
        meal_subtotal = 0
        for old_meal in old_meals:
            meal = db.query(Meal).filter(Meal.id == old_meal.meal_id).first()
            if meal:
                meal_subtotal += meal.price * old_meal.quantity
            db.delete(old_meal)
        
        # Add new meals
        new_meal_total = 0
        for meal_id in meal_ids:
            meal = db.query(Meal).filter(Meal.id == meal_id).first()
            if meal:
                booking_meal = BookingMeal(
                    booking_id=booking.id,
                    meal_id=meal_id
                )
                db.add(booking_meal)
                new_meal_total += meal.price
        
        # Update total amount
        booking.total_amount = booking.total_amount - meal_subtotal + new_meal_total
        
        db.commit()
        db.refresh(booking)
        
        return booking
