from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from database import Base

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(100), unique=True, index=True)
    state = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    population = Column(Integer, nullable=True)
    tier = Column(String(20), nullable=True)  # Tier-1, Tier-2, Tier-3
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LivabilityScore(Base):
    __tablename__ = "livability_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, index=True)
    overall_score = Column(Float)
    rank = Column(Integer)
    percentile = Column(Float, nullable=True)
    timestamp = Column(Date, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CategoryScore(Base):
    __tablename__ = "category_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, index=True)
    crime_score = Column(Float, nullable=True)
    healthcare_score = Column(Float, nullable=True)
    water_score = Column(Float, nullable=True)
    education_score = Column(Float, nullable=True)
    sanitation_score = Column(Float, nullable=True)
    pollution_score = Column(Float, nullable=True)
    traffic_score = Column(Float, nullable=True)
    cost_score = Column(Float, nullable=True)
    population_score = Column(Float, nullable=True)
    transport_score = Column(Float, nullable=True)
    timestamp = Column(Date, server_default=func.now())

class RawMetric(Base):
    __tablename__ = "raw_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, index=True)
    aqi = Column(Float, nullable=True)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    congestion_index = Column(Float, nullable=True)
    rent_affordability = Column(Float, nullable=True)
    crime_rate = Column(Float, nullable=True)
    literacy_rate = Column(Float, nullable=True)
    healthcare_facilities = Column(Integer, nullable=True)
    timestamp = Column(Date, server_default=func.now())
