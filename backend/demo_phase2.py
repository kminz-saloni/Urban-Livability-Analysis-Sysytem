"""
Phase 2 Demo Script

Demonstrates the complete analytics pipeline:
- Data Loading
- Normalization
- Scoring
- Ranking
- EDA Insights
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.data_processing import DataProcessingService
from data import get_sample_dataframe
import pandas as pd


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def main():
    """Run the phase 2 demo"""
    
    print_section("URBANPULSE IQ - PHASE 2: ANALYTICS CORE DEMO")
    
    # Initialize service
    print("Initializing Data Processing Service...")
    service = DataProcessingService()
    
    # Run full pipeline
    print("\nRunning complete pipeline...")
    results = service.get_full_pipeline_results()
    
    # Display results
    print_section("PROCESSING SUMMARY")
    print(f"✓ Cities Processed: {results['cities_processed']}")
    print(f"✓ Status: {results['status'].upper()}")
    
    print_section("LIVABILITY SCORE STATISTICS")
    stats = results['statistics']
    print(f"Mean Score:     {stats['mean_score']:.2f}")
    print(f"Median Score:   {stats['median_score']:.2f}")
    print(f"Std Deviation:  {stats['std_dev']:.2f}")
    print(f"Range:          {stats['min_score']:.2f} - {stats['max_score']:.2f}")
    
    print_section("TOP 10 CITIES BY LIVABILITY")
    for city in results['top_10']:
        print(f"  #{city['rank']:2d}  {city['city_name']:20s}  Score: {city['livability_score']:6.2f}  Tier: {city['tier']}")
    
    print_section("BOTTOM 5 CITIES")
    bottom_5 = results['rankings'][-5:]
    for city in bottom_5:
        print(f"  #{city['rank']:2d}  {city['city_name']:20s}  Score: {city['livability_score']:6.2f}  Tier: {city['tier']}")
    
    print_section("AI-GENERATED INSIGHTS")
    for i, insight in enumerate(results['insights'], 1):
        print(f"\n  {i}. {insight['title']}")
        print(f"     {insight['description']}")
        print(f"     Type: {insight['type'].upper()} | Confidence: {insight['confidence']:.0%}")
    
    # Get detailed city profile
    print_section("DETAILED CITY PROFILE: KOZHIKODE")
    profile = service.get_city_profile('Kozhikode')
    
    print(f"City: {profile['city_name']}, {profile['state']}")
    print(f"Rank: #{profile['rank']} | Score: {profile['livability_score']:.2f} | Percentile: {profile['percentile']:.1f}th")
    print(f"Tier Classification: {profile['tier']}")
    
    print("\nCategory Scores (0-100):")
    for category, score in profile['category_scores'].items():
        bar = "█" * int(score/10) + "░" * (10 - int(score/10))
        print(f"  {category:15s} {score:5.1f}  {bar}")
    
    print("\nRaw Metrics:")
    for metric, value in profile['raw_metrics'].items():
        print(f"  {metric:20s}: {value:.2f}")
    
    print("\nScore Contributions to Overall Livability:")
    for category, contribution in sorted(
        profile['score_contributions'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  {category:15s}: {contribution:6.2f} points")
    
    # Comparison
    print_section("CITY COMPARISON: TOP 3 VS BOTTOM 3")
    print("\nTOP 3 SCORES:")
    for city in results['top_10'][:3]:
        print(f"  {city['city_name']:20s} - {city['livability_score']:6.2f}")
    
    print("\nBOTTOM 3 SCORES:")
    for city in results['rankings'][-3:]:
        print(f"  {city['city_name']:20s} - {city['livability_score']:6.2f}")
    
    print_section("PHASE 2 COMPLETION STATUS")
    print("✓ Normalization Engine - COMPLETE")
    print("✓ Scoring Engine - COMPLETE")
    print("✓ EDA Processor - COMPLETE")
    print("✓ Data Processing Service - COMPLETE")
    print("✓ Rankings API - UPDATE WITH REAL DATA")
    print("✓ Sample Data (10 cities) - COMPLETE")
    
    print("\nAll Phase 2 components have been successfully implemented!")
    print("The system is now ready for Phase 3: Dashboard Development")
    
    print_section("API ENDPOINTS AVAILABLE")
    print("GET  /api/rankings           - Get all rankings")
    print("GET  /api/rankings/top       - Get top 10 cities")
    print("GET  /api/rankings/bottom    - Get bottom 10 cities")
    print("GET  /api/rankings/stats     - Get ranking statistics")
    print("GET  /api/rankings/insights  - Get AI insights")
    print("GET  /api/rankings/{city}    - Get city profile")
    print("GET  /api/rankings/by-tier/{tier} - Get cities by tier")


if __name__ == "__main__":
    main()
