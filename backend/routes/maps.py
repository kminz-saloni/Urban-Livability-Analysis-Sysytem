from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from data.sample_data import CITY_METRICS
from services.data_processing import get_data_service

router = APIRouter()

@router.get("/livability")
async def get_livability_map_data(db: Session = Depends(get_db)):
    """
    Get livability heatmap data with choropleths
    """
    service = get_data_service()
    results = service.get_full_pipeline_results()
    rankings = {r["city_name"]: r for r in results["rankings"]}

    features = []
    for city in CITY_METRICS:
        ranking = rankings.get(city["city_name"], {})
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "city": city["city_name"],
                    "state": city["state"],
                    "score": float(ranking.get("livability_score", 0)),
                    "rank": int(ranking.get("rank", 0)),
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [city["longitude"], city["latitude"]],
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}

@router.get("/aqi-layer")
async def get_aqi_layer(db: Session = Depends(get_db)):
    """
    Get AQI heat layer for map
    """
    aqi_data = [
        {
            "city": city["city_name"],
            "pm25": city["pm25"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
        }
        for city in CITY_METRICS
    ]
    return {"aqi_data": aqi_data}

@router.get("/crime-density")
async def get_crime_density_layer(db: Session = Depends(get_db)):
    """
    Get crime density layer
    """
    crime_data = [
        {
            "city": city["city_name"],
            "crime_rate": city["crime_rate"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
        }
        for city in CITY_METRICS
    ]
    return {"crime_data": crime_data}

@router.get("/water-stress")
async def get_water_stress_layer(db: Session = Depends(get_db)):
    """
    Get water stress layer
    """
    water_data = [
        {
            "city": city["city_name"],
            "groundwater_depletion": city["groundwater_depletion"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
        }
        for city in CITY_METRICS
    ]
    return {"water_data": water_data}
