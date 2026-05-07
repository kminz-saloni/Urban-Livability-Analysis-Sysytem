from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# City Schemas
class CityBase(BaseModel):
    city_name: str
    state: str
    latitude: float
    longitude: float
    population: Optional[int] = None
    tier: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Livability Score Schemas
class LivabilityScoreBase(BaseModel):
    city_id: int
    overall_score: float
    rank: int
    percentile: Optional[float] = None

class LivabilityScoreCreate(LivabilityScoreBase):
    pass

class LivabilityScoreResponse(LivabilityScoreBase):
    id: int
    timestamp: date

    class Config:
        from_attributes = True

# Category Score Schemas
class CategoryScoreBase(BaseModel):
    city_id: int
    crime_score: Optional[float] = None
    healthcare_score: Optional[float] = None
    water_score: Optional[float] = None
    education_score: Optional[float] = None
    sanitation_score: Optional[float] = None
    pollution_score: Optional[float] = None
    traffic_score: Optional[float] = None
    cost_score: Optional[float] = None
    population_score: Optional[float] = None
    transport_score: Optional[float] = None

class CategoryScoreCreate(CategoryScoreBase):
    pass

class CategoryScoreResponse(CategoryScoreBase):
    id: int
    timestamp: date

    class Config:
        from_attributes = True

# Raw Metric Schemas
class RawMetricBase(BaseModel):
    city_id: int
    aqi: Optional[float] = None
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    congestion_index: Optional[float] = None
    rent_affordability: Optional[float] = None
    crime_rate: Optional[float] = None
    literacy_rate: Optional[float] = None
    healthcare_facilities: Optional[int] = None

class RawMetricCreate(RawMetricBase):
    pass

class RawMetricResponse(RawMetricBase):
    id: int
    timestamp: date

    class Config:
        from_attributes = True

# Ranking Response
class CityRankingResponse(BaseModel):
    rank: int
    city_name: str
    state: str
    overall_score: float
    tier: Optional[str] = None
    crime_score: Optional[float] = None
    pollution_score: Optional[float] = None

# Comparison Request
class ComparisonRequest(BaseModel):
    city_ids: list[int]

# Analytics Response
class AnalyticsResponse(BaseModel):
    city_name: str
    metric: str
    value: float
    trend: Optional[str] = None
