from sqlalchemy.orm import Session
from ..models.station import Station
from ..core.exceptions import InvalidStationException


class StationService:
    """Service to handle station management"""
    
    @staticmethod
    def get_all_stations(db: Session) -> list:
        """Get all stations ordered by sequence"""
        stations = db.query(Station).order_by(Station.sequence).all()
        return stations
    
    @staticmethod
    def get_station_by_id(db: Session, station_id: int) -> Station:
        """Get station details by ID"""
        station = db.query(Station).filter(Station.id == station_id).first()
        if not station:
            raise InvalidStationException("Station not found")
        return station
    
    @staticmethod
    def get_station_by_name(db: Session, name: str) -> Station:
        """Get station details by name"""
        station = db.query(Station).filter(
            Station.name.ilike(name)
        ).first()
        if not station:
            raise InvalidStationException("Station not found")
        return station
    
    @staticmethod
    def create_station(
        db: Session,
        name: str,
        arrival_time: str,
        departure_time: str,
        distance_km: int,
        sequence: int
    ) -> Station:
        """Create a new station"""
        existing = db.query(Station).filter(Station.name == name).first()
        if existing:
            raise InvalidStationException("Station with this name already exists")
        
        station = Station(
            name=name,
            arrival_time=arrival_time,
            departure_time=departure_time,
            distance_km=distance_km,
            sequence=sequence
        )
        db.add(station)
        db.commit()
        db.refresh(station)
        return station
