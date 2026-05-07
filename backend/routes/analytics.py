from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.data_processing import get_data_service

router = APIRouter()

@router.get("/aqi")
async def get_aqi_analytics(db: Session = Depends(get_db)):
    """
    Get AQI and pollution analytics
    """
    return {
        "metrics": [
            {"city": "Patna", "pm25": 250, "aqi": "Severe"},
            {"city": "Delhi", "pm25": 180, "aqi": "Very Poor"},
            {"city": "Bengaluru", "pm25": 90, "aqi": "Moderate"},
        ]
    }

@router.get("/crime")
async def get_crime_analytics(db: Session = Depends(get_db)):
    """
    Get crime analytics
    """
    return {
        "metrics": [
            {"month": "Jan", "cases": 45},
            {"month": "Feb", "cases": 52},
            {"month": "Mar", "cases": 48},
        ]
    }

@router.get("/water")
async def get_water_analytics(db: Session = Depends(get_db)):
    """
    Get water intelligence
    """
    return {
        "message": "Water stress analysis coming soon"
    }

@router.get("/traffic")
async def get_traffic_analytics(db: Session = Depends(get_db)):
    """
    Get traffic intelligence
    """
    return {
        "message": "Traffic intelligence coming soon"
    }

@router.get("/correlation")
async def get_correlation_matrix(db: Session = Depends(get_db)):
    """
    Get correlation matrix for urban metrics
    """
    return {
        "correlations": {
            "pollution_health": 0.82,
            "population_crime": 0.75,
            "congestion_livability": -0.68,
        }
    }


@router.get("/anomalies")
async def get_anomaly_insights(db: Session = Depends(get_db)):
    """
    Get anomaly detection report for key metrics
    """
    service = get_data_service()
    service.get_full_pipeline_results()
    return {"anomalies": service.get_anomaly_report()}
