from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import CityRankingResponse
from services.data_processing import get_data_service

router = APIRouter()

# Initialize ranking data on startup
_rankings_cache = None


def get_rankings_data():
    """Get or generate rankings data"""
    global _rankings_cache
    if _rankings_cache is None:
        service = get_data_service()
        results = service.get_full_pipeline_results()
        _rankings_cache = results['rankings']
    return _rankings_cache


@router.get("/stats")
async def get_ranking_statistics(db: Session = Depends(get_db)):
    """
    Get ranking statistics
    """
    service = get_data_service()
    results = service.get_full_pipeline_results()
    return results['statistics']


@router.get("/insights")
async def get_ranking_insights(db: Session = Depends(get_db)):
    """
    Get AI-generated insights from rankings
    """
    service = get_data_service()
    results = service.get_full_pipeline_results()
    return {
        'insights': results['insights'],
        'total_cities': results['cities_processed']
    }


@router.get("/", response_model=list)
async def get_rankings(
    limit: int = Query(50, description="Number of rankings to return"),
    db: Session = Depends(get_db)
):
    """
    Get all city rankings with optional limit
    """
    rankings = get_rankings_data()
    return rankings[:limit]


@router.get("/top")
async def get_top_cities(
    limit: int = Query(10, description="Number of top cities"),
    db: Session = Depends(get_db)
):
    """
    Get top livability cities
    """
    rankings = get_rankings_data()
    return rankings[:limit]


@router.get("/bottom")
async def get_bottom_cities(
    limit: int = Query(10, description="Number of bottom cities"),
    db: Session = Depends(get_db)
):
    """
    Get bottom livability cities (most challenged)
    """
    rankings = get_rankings_data()
    return rankings[-limit:]


@router.get("/by-tier/{tier}")
async def get_cities_by_tier(
    tier: str,
    db: Session = Depends(get_db)
):
    """
    Get cities filtered by tier (Tier-1, Tier-2, Tier-3)
    """
    rankings = get_rankings_data()
    filtered = [r for r in rankings if r.get('tier') == tier]
    return filtered


@router.get("/{city_name}")
async def get_city_ranking(
    city_name: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed ranking and profile for a specific city
    """
    service = get_data_service()
    try:
        profile = service.get_city_profile(city_name)
        return profile
    except Exception as e:
        return {"error": str(e)}
