from sqlalchemy.orm import Session
from datetime import datetime
from ..models.booking import Booking, BookingMeal
from ..models.seat import Seat
from ..models.station import Station
from ..models.meal import Meal
from ..core.common import (
    BookingNotFoundException,
    InvalidStationException,
    CancellationNotAllowedException,
    InvalidBookingException,
    generate_booking_reference,
    generate_pnr
)
from ..utils.utils import (
    validate_email,
    validate_phone,
    validate_station_combination,
    calculate_refund_amount
)
from .seat_service import SeatService


class BookingService:
    """Service to handle booking logic"""
    
    @staticmethod
    def create_booking(
        db: Session,
        booking_data
    ) -> Booking:
        """
        Create a new booking with validation
        """
        # Validate input (Pydantic does most, but we check logic)
        
        # Get stations
        from_station = db.query(Station).filter(Station.name == booking_data.from_station).first()
        to_station = db.query(Station).filter(Station.name == booking_data.to_station).first()
        
        if not from_station or not to_station:
            raise InvalidStationException("One or both stations not found")
        
        # Validate station combination
        if not validate_station_combination(from_station.sequence, to_station.sequence):
            raise InvalidStationException(
                "From station must come before to station in the route"
            )
        
        journey_date_str = booking_data.travel_date.strftime("%Y-%m-%d")

        # Check availability for ALL seats
        for seat_id in booking_data.seats:
            SeatService.check_seat_availability(
                db, seat_id, from_station.id, to_station.id, journey_date_str
            )
        
        # Calculate price
        total_seat_price = 0
        for seat_id in booking_data.seats:
            total_seat_price += SeatService.calculate_seat_price(
                db, seat_id, from_station.id, to_station.id
            )
        
        # Calculate meal price
        total_meal_price = 0
        if booking_data.meals:
            for meal_item in booking_data.meals:
                meal = db.query(Meal).filter(Meal.id == meal_item.meal_id).first()
                if meal:
                    total_meal_price += (meal.price * meal_item.quantity)
        
        total_amount = total_seat_price + total_meal_price

        # Generate booking reference
        booking_reference = generate_booking_reference(
            from_station.name, to_station.name
        )
        pnr = generate_pnr()

        from ..services.prediction_service import PredictionService
        
        booking_date_obj = datetime.now().date()
        journey_date_obj = booking_data.travel_date
        
        confirmation_probability = PredictionService.predict_confirmation_probability(
            booking_date_obj,
            journey_date_obj,
            len(booking_data.seats)
        )
        
        # Create booking
        booking = Booking(
            booking_reference=booking_reference,
            pnr=pnr,
            user_name=booking_data.passenger_details.name,
            email=booking_data.passenger_details.email,
            phone=booking_data.passenger_details.contact,
            from_station_id=from_station.id,
            to_station_id=to_station.id,
            # seat_id removed
            booking_date=datetime.now().strftime("%Y-%m-%d"),
            journey_date=journey_date_str,
            status="CONFIRMED",
            total_amount=total_amount,
            confirmation_probability=confirmation_probability
        )
        
        db.add(booking)
        db.flush()  # Get booking ID
        
        # Block ALL seats
        for seat_id in booking_data.seats:
            SeatService.block_seat(
                db, seat_id, from_station.id, to_station.id, journey_date_str, booking.id
            )
        
        # Add meals
        if booking_data.meals:
            for meal_item in booking_data.meals:
                meal_id = meal_item.meal_id
                quantity = meal_item.quantity
                
                # Verify meal exists again just to be safe or skip
                booking_meal = BookingMeal(
                    booking_id=booking.id,
                    meal_id=meal_id,
                    quantity=quantity
                )
                db.add(booking_meal)
        
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
        
        # Release ALL seat
        from ..models.seat import SeatAvailability # Local import to avoid circular dependency if any
        
        booked_availability = db.query(SeatAvailability).filter(
            SeatAvailability.booked_by == booking.id
        ).all()
        
        for availability in booked_availability:
            db.delete(availability)
        
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

    @staticmethod
    def get_booking_response_object(db: Session, booking_id: int) -> dict:
        """
        Construct a detailed dictionary matching BookingResponse schema
        """
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise BookingNotFoundException("Booking not found")
        
        from ..models.seat import SeatAvailability # Local import

        # Get Stations
        from_st = db.query(Station).filter(Station.id == booking.from_station_id).first()
        to_st = db.query(Station).filter(Station.id == booking.to_station_id).first()
        
        # Get Seats
        booked_availability = db.query(SeatAvailability).filter(
            SeatAvailability.booked_by == booking.id
        ).all()
        
        seat_ids = {ba.seat_id for ba in booked_availability}
        seats = db.query(Seat).filter(Seat.id.in_(seat_ids)).all()
        seat_names = sorted([s.seat_number for s in seats])
        
        # Get Meals
        meals = []
        for bm in booking.meals:
            meals.append({
                "meal_id": bm.meal_id,
                "quantity": bm.quantity
            })
            
        return {
            "booking_id": booking.booking_reference,
            "pnr": booking.pnr,
            "status": booking.status,
            "total_amount": booking.total_amount,
            "confirmation_probability": booking.confirmation_probability,
            "seats": seat_names,
            "meals": meals,
            "journey_details": {
                "from_station": from_st.name,
                "to_station": to_st.name,
                "date": datetime.strptime(booking.journey_date, "%Y-%m-%d").date(),
                "departure_time": from_st.departure_time,
                "arrival_time": to_st.arrival_time,
                "duration": "TBD"
            },
            "passenger_details": {
                "name": booking.user_name,
                "contact": booking.phone,
                "email": booking.email
            },
            "created_at": booking.created_at
        }
