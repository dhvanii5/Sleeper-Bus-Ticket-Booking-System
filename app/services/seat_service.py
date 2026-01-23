"""Seat Service - Business logic for seat availability and pricing"""

from sqlalchemy.orm import Session
from datetime import datetime
from ..models.seat import Seat, SeatAvailability
from ..models.station import Station
from ..core.common import SeatNotAvailableException, DoubleBookingException
from ..utils.utils import calculate_distance_between_stations, get_distance_multiplier, get_seat_type_multiplier


class SeatService:
    """Handles seat availability checks, booking, and dynamic pricing"""
    
    @staticmethod
    def get_available_seats(
        db: Session,
        from_station_id: int,
        to_station_id: int,
        journey_date: str
    ) -> list:
        """
        Find seats available for a specific route and date
        Prevents double-booking by checking for overlapping route segments
        """
        # Parse date string to date object
        dt_journey_date = datetime.strptime(journey_date, "%Y-%m-%d").date()

        # Get station positions in route sequence
        from_seq = db.query(Station.sequence).filter(Station.id == from_station_id).scalar()
        to_seq = db.query(Station.sequence).filter(Station.id == to_station_id).scalar()
        
        if from_seq is None or to_seq is None:
            return []  # Invalid station IDs

        # Find seats booked on overlapping route segments for this date
        # Overlap occurs when: existing_start < new_end AND existing_end > new_start
        overlapping_bookings = db.query(SeatAvailability).filter(
            SeatAvailability.journey_date == dt_journey_date,
            SeatAvailability.is_booked == True,
            SeatAvailability.from_station_id < to_seq,  # Existing booking starts before our destination
            SeatAvailability.to_station_id > from_seq   # Existing booking ends after our origin
        ).all()
        
        # Collect all seat IDs that are blocked
        blocked_seat_ids = {record.seat_id for record in overlapping_bookings}
        
        # Return only operational seats that aren't blocked
        available_seats = db.query(Seat).filter(
            Seat.is_available == True,  # Seat is operational
            ~Seat.id.in_(blocked_seat_ids)  # Seat is not blocked for this route
        ).all()
        
        return available_seats
    
    @staticmethod
    def check_seat_availability(
        db: Session,
        seat_number: str,
        from_station_id: int,
        to_station_id: int,
        journey_date: str
    ) -> bool:
        """
        Verify a specific seat can be booked for given route and date
        Raises exception if seat is unavailable or already booked
        """
        # Parse date string
        dt_journey_date = datetime.strptime(journey_date, "%Y-%m-%d").date()

        # Verify seat exists and is operational
        seat = db.query(Seat).filter(Seat.seat_number == seat_number).first()
        if not seat or not seat.is_available:
            raise SeatNotAvailableException("Seat does not exist or is not available")
        
        # Get station sequence numbers for overlap detection
        from_seq = db.query(Station.sequence).filter(Station.id == from_station_id).scalar()
        to_seq = db.query(Station.sequence).filter(Station.id == to_station_id).scalar()
        
        # Fetch all existing bookings for this seat on this date
        existing_bookings = db.query(SeatAvailability).join(
            Station, SeatAvailability.from_station_id == Station.id
        ).filter(
            SeatAvailability.seat_id == seat.id,
            SeatAvailability.journey_date == dt_journey_date,
            SeatAvailability.is_booked == True
        ).all()
        
        # Check each existing booking for route overlap
        for booking in existing_bookings:
            # Get sequence numbers of the existing booking's route
            existing_from_seq = db.query(Station.sequence).filter(
                Station.id == booking.from_station_id
            ).scalar()
            existing_to_seq = db.query(Station.sequence).filter(
                Station.id == booking.to_station_id
            ).scalar()
            
            # Detect overlap: new route overlaps if it starts before existing ends AND ends after existing starts
            if from_seq < existing_to_seq and to_seq > existing_from_seq:
                raise DoubleBookingException(
                    f"Seat is already booked for overlapping route segment"
                )
        
        if existing_bookings:
            raise DoubleBookingException("Seat is already booked for this route segment")
        
        return True
    
    @staticmethod
    def block_seat(
        db: Session,
        seat_number: str,
        from_station_id: int,
        to_station_id: int,
        journey_date: str,
        booking_id: int
    ):
        """Reserve a seat for a confirmed booking (creates SeatAvailability record)"""
        # Parse date string
        dt_journey_date = datetime.strptime(journey_date, "%Y-%m-%d").date()
        
        # Convert seat number to internal seat ID
        seat = db.query(Seat).filter(Seat.seat_number == seat_number).first()
        if not seat:
            raise SeatNotAvailableException(f"Seat {seat_number} not found")
        seat_id = seat.id

        # Create booking record to block this seat for this route segment
        seat_availability = SeatAvailability(
            seat_id=seat_id,
            from_station_id=from_station_id,
            to_station_id=to_station_id,
            journey_date=dt_journey_date,
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
        """Unblock a seat (used when cancelling a booking)"""
        # Parse date string
        dt_journey_date = datetime.strptime(journey_date, "%Y-%m-%d").date()

        # Find and delete the blocking record
        seat_availability = db.query(SeatAvailability).filter(
            SeatAvailability.seat_id == seat_id,
            SeatAvailability.from_station_id == from_station_id,
            SeatAvailability.to_station_id == to_station_id,
            SeatAvailability.journey_date == dt_journey_date,
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
        Calculate dynamic price: Base Price × Distance Multiplier × Seat Type Multiplier
        Longer distances and lower berths cost more
        """
        # Fetch seat and station details
        seat = db.query(Seat).filter(Seat.id == seat_id).first()
        from_station = db.query(Station).filter(Station.id == from_station_id).first()
        to_station = db.query(Station).filter(Station.id == to_station_id).first()
        
        # Calculate distance traveled (in km)
        distance = calculate_distance_between_stations(
            from_station.distance_km,
            to_station.distance_km
        )
        
        distance_multiplier = get_distance_multiplier(distance)
        seat_type_multiplier = get_seat_type_multiplier(seat.seat_type)
        
        final_price = int(seat.base_price * distance_multiplier * seat_type_multiplier)
        return final_price
