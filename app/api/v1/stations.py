from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...api.dependencies import get_db
from ...services.station_service import StationService
from ...schemas.schemas import Station, StationsResponse

router = APIRouter()


@router.get("/stations", response_model=StationsResponse)
async def get_all_stations(db: Session = Depends(get_db)):
    """
    Get list of all stations on the Ahmedabad-Mumbai route.
    Returns stations in sequence order with timing information.
    """
    stations = StationService.get_all_stations(db)
    
    return {
        "route": "Ahmedabad → Mumbai", # Hardcoded or generated
        "stations": stations
    }


@router.get("/{station_id}")
async def get_station(station_id: int, db: Session = Depends(get_db)):
    """Get station details by ID"""
    station = StationService.get_station_by_id(db, station_id)
    return station


