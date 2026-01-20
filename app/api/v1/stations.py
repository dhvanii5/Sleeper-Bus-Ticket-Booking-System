from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...api.dependencies import get_db
from ...services.station_service import StationService
from ...schemas.seat import Station, StationCreate

router = APIRouter()


@router.get("/")
async def get_all_stations(db: Session = Depends(get_db)):
    """Get all stations in the route"""
    stations = StationService.get_all_stations(db)
    return stations


@router.get("/{station_id}")
async def get_station(station_id: int, db: Session = Depends(get_db)):
    """Get station details by ID"""
    station = StationService.get_station_by_id(db, station_id)
    return station


@router.post("/", response_model=Station)
async def create_station(
    station: StationCreate,
    db: Session = Depends(get_db)
):
    """Create a new station"""
    new_station = StationService.create_station(
        db,
        station.name,
        station.arrival_time,
        station.departure_time,
        station.distance_km,
        station.sequence
    )
    return new_station