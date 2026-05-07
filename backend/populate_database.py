"""
Database Population Script
Creates tables and populates Supabase with sample city data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import Base, engine, SessionLocal
from models import City, LivabilityScore, CategoryScore, RawMetric
from data.sample_data import CITY_METRICS

from datetime import datetime
def create_tables():
    """Create all tables in Supabase"""
    print("🔧 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        raise

def populate_cities(db):
    """Insert city data"""
    print("\n📍 Populating cities...")
    
    for city_data in CITY_METRICS:
        try:
            # Check if city already exists
            existing = db.query(City).filter(
                City.city_name == city_data['city_name']
            ).first()
            
            if not existing:
                city = City(
                    city_name=city_data['city_name'],
                    state=city_data['state'],
                    latitude=city_data['latitude'],
                    longitude=city_data['longitude'],
                    population=city_data.get('population'),
                    tier=city_data.get('tier'),
                )
                db.add(city)
                print(f"  ✓ Added: {city_data['city_name']}, {city_data['state']}")
            else:
                print(f"  ⊘ Already exists: {city_data['city_name']}")
        except Exception as e:
            print(f"  ✗ Error adding {city_data['city_name']}: {e}")
    
    db.commit()
    print(f"✓ Cities population complete")

def populate_raw_metrics(db):
    """Insert raw metrics"""
    print("\n📊 Populating raw metrics...")
    
    cities = db.query(City).all()
    
    for i, city_data in enumerate(CITY_METRICS):
        try:
            city = cities[i] if i < len(cities) else None
            if not city:
                continue
            
            # Check if metrics already exist
            existing = db.query(RawMetric).filter(
                RawMetric.city_id == city.id
            ).first()
            
            if not existing:
                metric = RawMetric(
                    city_id=city.id,
                    aqi=city_data.get('aqi'),
                    pm25=city_data.get('pm25'),
                    pm10=city_data.get('pm10'),
                    congestion_index=city_data.get('congestion_index'),
                    rent_affordability=city_data.get('rent_affordability'),
                    crime_rate=city_data.get('crime_rate'),
                    literacy_rate=city_data.get('literacy_rate'),
                    healthcare_facilities=city_data.get('healthcare_score'),
                )
                db.add(metric)
                print(f"  ✓ Added metrics for: {city.city_name}")
            else:
                print(f"  ⊘ Metrics exist for: {city.city_name}")
        except Exception as e:
            print(f"  ✗ Error adding metrics: {e}")
    
    db.commit()
    print(f"✓ Raw metrics population complete")

def populate_category_scores(db):
    """Insert category scores"""
    print("\n🎯 Populating category scores...")
    
    cities = db.query(City).all()
    
    for i, city_data in enumerate(CITY_METRICS):
        try:
            city = cities[i] if i < len(cities) else None
            if not city:
                continue
            
            # Check if scores already exist
            existing = db.query(CategoryScore).filter(
                CategoryScore.city_id == city.id
            ).first()
            
            if not existing:
                score = CategoryScore(
                    city_id=city.id,
                    crime_score=100 - (city_data.get('crime_rate', 0) * 10),
                    healthcare_score=city_data.get('healthcare_score', 75),
                    water_score=city_data.get('water_quality', 70),
                    education_score=city_data.get('education_score', 80),
                    sanitation_score=city_data.get('sanitation_score', 75),
                    pollution_score=100 - (city_data.get('aqi', 50) * 0.5),
                    traffic_score=100 - (city_data.get('congestion_index', 40) * 1.5),
                    cost_score=city_data.get('rent_affordability', 50),
                    population_score=75,
                    transport_score=city_data.get('transport_facilities', 75),
                )
                db.add(score)
                print(f"  ✓ Added category scores for: {city.city_name}")
            else:
                print(f"  ⊘ Category scores exist for: {city.city_name}")
        except Exception as e:
            print(f"  ✗ Error adding category scores: {e}")
    
    db.commit()
    print(f"✓ Category scores population complete")

def populate_livability_scores(db):
    """Insert livability scores with ranking"""
    print("\n⭐ Populating livability scores...")
    
    try:
        categories = db.query(CategoryScore).all()
        cities = db.query(City).all()
        
        scores = []
        for i, cat_score in enumerate(categories):
            city = next((c for c in cities if c.id == cat_score.city_id), None)
            if city:
                # Calculate overall score (average of all category scores)
                overall = (
                    (cat_score.crime_score or 0) +
                    (cat_score.healthcare_score or 0) +
                    (cat_score.water_score or 0) +
                    (cat_score.education_score or 0) +
                    (cat_score.sanitation_score or 0) +
                    (cat_score.pollution_score or 0) +
                    (cat_score.traffic_score or 0) +
                    (cat_score.cost_score or 0) +
                    (cat_score.population_score or 0) +
                    (cat_score.transport_score or 0)
                ) / 10
                
                scores.append({
                    'city_id': city.id,
                    'overall_score': round(overall, 2),
                    'city_name': city.city_name
                })
        
        # Sort by score and assign ranks
        scores_sorted = sorted(scores, key=lambda x: x['overall_score'], reverse=True)
        
        for rank, score_data in enumerate(scores_sorted, 1):
            existing = db.query(LivabilityScore).filter(
                LivabilityScore.city_id == score_data['city_id']
            ).first()
            
            if not existing:
                liv_score = LivabilityScore(
                    city_id=score_data['city_id'],
                    overall_score=score_data['overall_score'],
                    rank=rank,
                    percentile=round((rank / len(scores_sorted)) * 100, 2)
                )
                db.add(liv_score)
                print(f"  ✓ Rank #{rank}: {score_data['city_name']} ({score_data['overall_score']}/100)")
            else:
                print(f"  ⊘ Score exists for: {score_data['city_name']}")
        
        db.commit()
        print(f"✓ Livability scores population complete")
    except Exception as e:
        print(f"✗ Error populating livability scores: {e}")
        raise

def main():
    """Run the complete population process"""
    print("\n" + "="*70)
    print("  SUPABASE DATABASE POPULATION SCRIPT")
    print("="*70)
    
    db = SessionLocal()
    
    try:
        # Step 1: Create tables
        create_tables()
        
        # Step 2: Populate data
        populate_cities(db)
        populate_raw_metrics(db)
        populate_category_scores(db)
        populate_livability_scores(db)
        
        # Step 3: Display summary
        print("\n" + "="*70)
        print("  POPULATION SUMMARY")
        print("="*70)
        
        total_cities = db.query(City).count()
        total_metrics = db.query(RawMetric).count()
        total_categories = db.query(CategoryScore).count()
        total_scores = db.query(LivabilityScore).count()
        
        print(f"\n✓ Cities:            {total_cities}")
        print(f"✓ Raw Metrics:       {total_metrics}")
        print(f"✓ Category Scores:   {total_categories}")
        print(f"✓ Livability Scores: {total_scores}")
        
        print("\n" + "="*70)
        print("  ✓ DATABASE POPULATION COMPLETE!")
        print("="*70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        db.rollback()
        return 1
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(main())
