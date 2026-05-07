from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CityResponse

router = APIRouter()

MOCK_CITIES = [
    {
        "id": 1,
        "city_name": "Kozhikode",
        "state": "Kerala",
        "latitude": 11.2588,
        "longitude": 75.7804,
        "tier": "Tier-2",
        "created_at": "2026-05-01T00:00:00"
    },
    {
        "id": 2,
        "city_name": "Coimbatore",
        "state": "Tamil Nadu",
        "latitude": 11.0060,
        "longitude": 76.9855,
        "tier": "Tier-2",
        "created_at": "2026-05-01T00:00:00"
    },
    {
        "id": 3,
        "city_name": "Kochi",
        "state": "Kerala",
        "latitude": 9.9312,
        "longitude": 76.2673,
        "tier": "Tier-2",
        "created_at": "2026-05-01T00:00:00"
    },
]

@router.get("/", response_model=list[CityResponse])
async def get_cities(db: Session = Depends(get_db)):
    """
    Get all cities
    """
    return MOCK_CITIES

@router.get("/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    """
    Get a specific city by ID
    """
    for city in MOCK_CITIES:
        if city["id"] == city_id:
            return city
    return {"error": "City not found"}

@router.post("/", response_model=CityResponse)
async def create_city(city: CityResponse, db: Session = Depends(get_db)):
    """
    Create a new city
    """
    return city
