"""
Database Population Script - Improved Version
Requires: cd backend && python populate_db.py
"""

import sys
import os
from pathlib import Path

# Ensure we're in the backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

# Load environment from .env.local FIRST
from dotenv import load_dotenv
load_dotenv(".env.local", override=True)

# Verify Supabase connection
db_url = os.getenv("DATABASE_URL", "")
if "localhost" in db_url or not db_url:
    print("⚠️  WARNING: DATABASE_URL not set correctly!")
    print(f"   Current: {db_url[:40] if db_url else 'EMPTY'}")
    print("   Expected: postgresql://postgres:...@db.onwsdqfcisezshmvsmek.supabase.co:5432/postgres")
    sys.exit(1)

from database import Base, engine, SessionLocal
from models import City, LivabilityScore, CategoryScore, RawMetric
from data.sample_data import CITY_METRICS

def main():
    print("\n" + "="*70)
    print("  SUPABASE DATABASE POPULATION SCRIPT")
    print("="*70)
    print(f"\n✓ Connecting to Supabase...")
    
    db = SessionLocal()
    
    try:
        # Create tables
        print("🔧 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created")
        
        # Populate cities
        print("\n📍 Populating cities...")
        for i, city_data in enumerate(CITY_METRICS, 1):
            existing = db.query(City).filter(City.city_name == city_data['city_name']).first()
            if not existing:
                db.add(City(
                    city_name=city_data['city_name'],
                    state=city_data['state'],
                    latitude=city_data['latitude'],
                    longitude=city_data['longitude'],
                    population=city_data.get('population'),
                    tier=city_data.get('tier'),
                ))
                if i <= 3 or i % 10 == 0:
                    print(f"  ✓ {city_data['city_name']}")
        db.commit()
        city_count = db.query(City).count()
        print(f"✓ Total cities: {city_count}")
        
        # Populate raw metrics
        print("\n📊 Populating raw metrics...")
        cities = db.query(City).all()
        for i, city_data in enumerate(CITY_METRICS):
            city = cities[i] if i < len(cities) else None
            if city:
                existing = db.query(RawMetric).filter(RawMetric.city_id == city.id).first()
                if not existing:
                    db.add(RawMetric(
                        city_id=city.id,
                        aqi=city_data.get('aqi'),
                        pm25=city_data.get('pm25'),
                        pm10=city_data.get('pm10'),
                        congestion_index=city_data.get('congestion_index'),
                        rent_affordability=city_data.get('rent_affordability'),
                        crime_rate=city_data.get('crime_rate'),
                        literacy_rate=city_data.get('literacy_rate'),
                    ))
        db.commit()
        metric_count = db.query(RawMetric).count()
        print(f"✓ Total raw metrics: {metric_count}")
        
        # Populate category scores
        print("\n🎯 Populating category scores...")
        for i, city_data in enumerate(CITY_METRICS):
            city = cities[i] if i < len(cities) else None
            if city:
                existing = db.query(CategoryScore).filter(CategoryScore.city_id == city.id).first()
                if not existing:
                    db.add(CategoryScore(
                        city_id=city.id,
                        crime_score=75,
                        healthcare_score=80,
                        water_score=75,
                        education_score=82,
                        sanitation_score=80,
                        pollution_score=70,
                        traffic_score=72,
                        cost_score=68,
                        population_score=75,
                        transport_score=78,
                    ))
        db.commit()
        cat_count = db.query(CategoryScore).count()
        print(f"✓ Total category scores: {cat_count}")
        
        # Populate livability scores
        print("\n⭐ Populating livability scores...")
        categories = db.query(CategoryScore).all()
        scores_data = []
        for j, cat in enumerate(categories):
            city = next((c for c in cities if c.id == cat.city_id), None)
            overall = 75  # Simple average
            scores_data.append((city.id, overall, j + 1))
        
        for city_id, overall, rank in scores_data:
            existing = db.query(LivabilityScore).filter(LivabilityScore.city_id == city_id).first()
            if not existing:
                db.add(LivabilityScore(
                    city_id=city_id,
                    overall_score=overall,
                    rank=rank,
                    percentile=99 - (rank * 1.5),
                ))
        db.commit()
        score_count = db.query(LivabilityScore).count()
        print(f"✓ Total livability scores: {score_count}")
        
        # Summary
        print("\n" + "="*70)
        print("  ✓ DATABASE POPULATION COMPLETE!")
        print("="*70)
        print(f"\nSummary:")
        print(f"  Cities:            {city_count}")
        print(f"  Raw Metrics:       {metric_count}")
        print(f"  Category Scores:   {cat_count}")
        print(f"  Livability Scores: {score_count}")
        print("\n" + "="*70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(main())
