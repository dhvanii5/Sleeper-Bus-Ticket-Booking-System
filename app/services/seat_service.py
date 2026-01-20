from sqlalchemy.orm import Session
from datetime import datetime
from ..models.seat import Seat, SeatAvailability
from ..models.station import Station
from ..core.exceptions import SeatNotAvailableException, DoubleBookingException
from ..utils.helpers import calculate_distance_between_stations, get_distance_multiplier, get_seat_type_multiplier


class SeatService:
    """Service to handle seat availability and pricing logic"""
    
    @staticmethod
    def get_available_seats(
        db: Session,
        from_station_id: int,
        to_station_id: int,
        journey_date: str
    ) -> list:
        """
        Get available seats for a specific route and date.
        A seat is available if it's not booked for any segment within the route.
        """
        # Get all seat availability records for the route segments
        booked_seats = db.query(SeatAvailability).filter(
            SeatAvailability.from_station_id >= (
                db.query(Station.sequence).filter(Station.id == from_station_id).scalar()
            ),
            SeatAvailability.to_station_id <= (
                db.query(Station.sequence).filter(Station.id == to_station_id).scalar()
            ),
            SeatAvailability.journey_date == journey_date,
            SeatAvailability.is_booked == True
        ).all()
        
        booked_seat_ids = {record.seat_id for record in booked_seats}
        
        # Get all seats and filter out booked ones
        available_seats = db.query(Seat).filter(
            Seat.is_available == True,
            ~Seat.id.in_(booked_seat_ids)
        ).all()
        
        return available_seats
    
    @staticmethod
    def check_seat_availability(
        db: Session,
        seat_id: int,
        from_station_id: int,
        to_station_id: int,
        journey_date: str
    ) -> bool:
        """
        Check if a specific seat is available for the given route and date.
        """
        # Check if seat exists and is marked as available
        seat = db.query(Seat).filter(Seat.id == seat_id).first()
        if not seat or not seat.is_available:
            raise SeatNotAvailableException("Seat does not exist or is not available")
        
        # Check if there's any booking conflict for this seat
        from_seq = db.query(Station.sequence).filter(Station.id == from_station_id).scalar()
        to_seq = db.query(Station.sequence).filter(Station.id == to_station_id).scalar()
        
        existing_bookings = db.query(SeatAvailability).filter(
            SeatAvailability.seat_id == seat_id,
            SeatAvailability.journey_date == journey_date,
            SeatAvailability.is_booked == True,
            # Check for overlapping routes
            SeatAvailability.from_station_id < to_seq,
            SeatAvailability.to_station_id > from_seq
        ).first()
        
        if existing_bookings:
            raise DoubleBookingException("Seat is already booked for this route segment")
        
        return True
    
    @staticmethod
    def block_seat(
        db: Session,
        seat_id: int,
        from_station_id: int,
        to_station_id: int,
        journey_date: str,
        booking_id: int
    ):
        """Block a seat for a booking"""
        seat_availability = SeatAvailability(
            seat_id=seat_id,
            from_station_id=from_station_id,
            to_station_id=to_station_id,
            journey_date=journey_date,
            is_booked=True,
            booked_by=booking_id
        )
        db.add(seat_availability)
        db.commit()
    
    @staticmethod
    def release_seat(
        db: Session,
        seat_id: int,
        from_station_id: int,
        to_station_id: int,
        journey_date: str
    ):
        """Release a blocked seat"""
        seat_availability = db.query(SeatAvailability).filter(
            SeatAvailability.seat_id == seat_id,
            SeatAvailability.from_station_id == from_station_id,
            SeatAvailability.to_station_id == to_station_id,
            SeatAvailability.journey_date == journey_date,
            SeatAvailability.is_booked == True
        ).first()
        
        if seat_availability:
            db.delete(seat_availability)
            db.commit()
    
    @staticmethod
    def calculate_seat_price(
        db: Session,
        seat_id: int,
        from_station_id: int,
        to_station_id: int
    ) -> int:
        """
        Calculate dynamic price based on seat type and distance.
        Price = Base Price × Distance Multiplier × Seat Type Multiplier
        """
        seat = db.query(Seat).filter(Seat.id == seat_id).first()
        
        from_station = db.query(Station).filter(Station.id == from_station_id).first()
        to_station = db.query(Station).filter(Station.id == to_station_id).first()
        
        distance = calculate_distance_between_stations(
            from_station.distance_km,
            to_station.distance_km
        )
        
        distance_multiplier = get_distance_multiplier(distance)
        seat_type_multiplier = get_seat_type_multiplier(seat.seat_type)
        
        final_price = int(seat.base_price * distance_multiplier * seat_type_multiplier)
        return final_price
