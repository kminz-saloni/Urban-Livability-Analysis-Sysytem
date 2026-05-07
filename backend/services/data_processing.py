"""
Data Processing Service for UrbanPulse IQ

Orchestrates the pipeline: Raw Data → Normalize → Score → Rank
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import date

from analytics.normalization import NormalizationEngine, METRIC_TYPES, METRIC_BOUNDS
from analytics.scoring import ScoringEngine, WeightConfig
from analytics.eda_processor import EDAProcessor
from data.sample_data import get_sample_dataframe


class DataProcessingService:
    """
    Complete data processing pipeline for urban livability scoring.
    """

    def __init__(self):
        """Initialize the processing service"""
        self.normalization_engine = NormalizationEngine()
        self.scoring_engine = ScoringEngine()
        self.eda_processor = EDAProcessor()
        self.processed_data = None
        self.rankings = None

    def process_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw data through the complete pipeline
        
        Args:
            df: Raw data DataFrame
        
        Returns:
            Processed DataFrame with normalized scores and rankings
        """
        # Make a copy to avoid modifying original
        data = df.copy()
        
        # Step 1: Handle missing values
        print("Step 1: Handling missing values...")
        for col in data.select_dtypes(include=[np.number]).columns:
            missing_count = data[col].isna().sum()
            if missing_count > 0:
                data[col] = self.normalization_engine.handle_missing_values(
                    data[col].tolist(),
                    strategy='median'
                )
        
        # Step 2: Normalize individual metrics
        print("Step 2: Normalizing metrics...")
        
        # Crime (negative - lower is better)
        if 'crime_rate' in data.columns:
            data['crime_score'] = self.normalization_engine.normalize_negative_metric(
                data['crime_rate'].values,
                *METRIC_BOUNDS.get('crime_rate', (None, None))
            )
        
        # Healthcare (positive - higher is better)
        if 'healthcare_score' in data.columns:
            data['healthcare_score'] = self.normalization_engine.normalize_positive_metric(
                data['healthcare_score'].values,
                0, 100
            )
        
        # Water quality (positive)
        if 'water_quality' in data.columns:
            data['water_score'] = self.normalization_engine.normalize_positive_metric(
                data['water_quality'].values,
                0, 100
            )
        else:
            data['water_score'] = 50.0
        
        # Education (positive)
        if 'education_score' in data.columns:
            data['education_score'] = self.normalization_engine.normalize_positive_metric(
                data['education_score'].values,
                0, 100
            )
        
        # Sanitation (positive)
        if 'sanitation_score' in data.columns:
            data['sanitation_score'] = self.normalization_engine.normalize_positive_metric(
                data['sanitation_score'].values,
                0, 100
            )
        
        # Pollution - AQI (negative - lower is better)
        if 'aqi' in data.columns:
            data['pollution_score'] = self.normalization_engine.normalize_negative_metric(
                data['aqi'].values,
                0, 500
            )
        
        # Traffic congestion (negative)
        if 'congestion_index' in data.columns:
            data['traffic_score'] = self.normalization_engine.normalize_negative_metric(
                data['congestion_index'].values,
                0, 100
            )
        
        # Cost affordability (negative - higher rent = worse)
        if 'rent_affordability' in data.columns:
            data['cost_score'] = self.normalization_engine.normalize_negative_metric(
                data['rent_affordability'].values,
                0, 100
            )
        
        # Population (neutral - score by city size distribution)
        if 'population' in data.columns:
            data['population_score'] = self.normalization_engine.normalize_positive_metric(
                data['population'].values
            )
        else:
            data['population_score'] = 50.0
        
        # Transport (positive)
        if 'transport_facilities' in data.columns:
            data['transport_score'] = self.normalization_engine.normalize_positive_metric(
                data['transport_facilities'].values,
                0, 100
            )
        else:
            data['transport_score'] = 50.0
        
        self.processed_data = data
        return data

    def calculate_livability_scores(self, processed_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate livability scores for all cities
        
        Args:
            processed_df: DataFrame with normalized scores
        
        Returns:
            DataFrame with livability scores and rankings
        """
        print("Step 3: Calculating weighted livability scores...")
        
        data = processed_df.copy()
        
        # Calculate overall scores
        scores = []
        for idx, row in data.iterrows():
            score = self.scoring_engine.calculate_score(
                crime_score=row.get('crime_score', 50),
                healthcare_score=row.get('healthcare_score', 50),
                water_score=row.get('water_score', 50),
                education_score=row.get('education_score', 50),
                sanitation_score=row.get('sanitation_score', 50),
                pollution_score=row.get('pollution_score', 50),
                traffic_score=row.get('traffic_score', 50),
                cost_score=row.get('cost_score', 50),
                population_score=row.get('population_score', 50),
                transport_score=row.get('transport_score', 50)
            )
            scores.append(score)
        
        data['livability_score'] = scores
        
        # Step 4: Generate rankings
        print("Step 4: Generating rankings...")
        
        rankings = self.scoring_engine.rank_cities(
            city_names=data['city_name'].tolist(),
            scores=data['livability_score'].tolist()
        )
        
        # Add city tier classification
        rankings['tier'] = rankings['livability_score'].apply(self.scoring_engine.get_city_tier)
        
        # Merge back with original data
        result = data.merge(rankings[['city_name', 'rank', 'percentile', 'tier']], on='city_name')
        result = result.sort_values('rank')
        
        self.rankings = result
        return result

    def get_full_pipeline_results(self, df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Run complete pipeline and return results
        
        Args:
            df: Input DataFrame (uses sample data if not provided)
        
        Returns:
            Dictionary with processing results
        """
        if df is None:
            print("Loading sample data...")
            df = get_sample_dataframe()
        
        # Process data
        processed = self.process_raw_data(df)
        
        # Calculate scores
        final_rankings = self.calculate_livability_scores(processed)
        
        # Generate insights
        print("Step 5: Generating insights...")
        insights = self.eda_processor.generate_research_insights(final_rankings)
        
        return {
            'status': 'success',
            'cities_processed': len(final_rankings),
            'rankings': final_rankings.to_dict('records'),
            'top_10': final_rankings.head(10).to_dict('records'),
            'bottom_10': final_rankings.tail(10).to_dict('records'),
            'insights': [
                {
                    'title': i.title,
                    'description': i.description,
                    'type': i.insight_type.value,
                    'confidence': i.confidence
                } for i in insights
            ],
            'statistics': {
                'mean_score': float(final_rankings['livability_score'].mean()),
                'median_score': float(final_rankings['livability_score'].median()),
                'std_dev': float(final_rankings['livability_score'].std()),
                'min_score': float(final_rankings['livability_score'].min()),
                'max_score': float(final_rankings['livability_score'].max())
            }
        }

    def get_correlation_matrix(self) -> Dict:
        """
        Get correlation matrix from processed data
        
        Returns:
            Correlation matrix as dictionary
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Run pipeline first.")
        
        numeric_cols = self.processed_data.select_dtypes(include=[np.number]).columns
        correlation = self.processed_data[numeric_cols].corr()
        
        return correlation.to_dict()

    def get_city_profile(self, city_name: str) -> Dict:
        """
        Get detailed profile for a city
        
        Args:
            city_name: Name of the city
        
        Returns:
            City profile with all metrics
        """
        if self.rankings is None:
            raise ValueError("No rankings available. Run pipeline first.")
        
        city_data = self.rankings[self.rankings['city_name'] == city_name]
        
        if city_data.empty:
            return {'error': f'City {city_name} not found'}
        
        city = city_data.iloc[0]
        
        # Calculate contributions
        contributions = self.scoring_engine.calculate_score_contribution(
            crime_score=city.get('crime_score', 50),
            healthcare_score=city.get('healthcare_score', 50),
            water_score=city.get('water_score', 50),
            education_score=city.get('education_score', 50),
            sanitation_score=city.get('sanitation_score', 50),
            pollution_score=city.get('pollution_score', 50),
            traffic_score=city.get('traffic_score', 50),
            cost_score=city.get('cost_score', 50),
            population_score=city.get('population_score', 50),
            transport_score=city.get('transport_score', 50)
        )
        
        return {
            'city_name': city['city_name'],
            'state': city['state'],
            'rank': int(city['rank']),
            'livability_score': float(city['livability_score']),
            'percentile': float(city['percentile']),
            'tier': city['tier'],
            'category_scores': {
                'crime': float(city.get('crime_score', 50)),
                'healthcare': float(city.get('healthcare_score', 50)),
                'water': float(city.get('water_score', 50)),
                'education': float(city.get('education_score', 50)),
                'sanitation': float(city.get('sanitation_score', 50)),
                'pollution': float(city.get('pollution_score', 50)),
                'traffic': float(city.get('traffic_score', 50)),
                'cost': float(city.get('cost_score', 50)),
                'population': float(city.get('population_score', 50)),
                'transport': float(city.get('transport_score', 50))
            },
            'score_contributions': contributions,
            'raw_metrics': {
                'aqi': float(city.get('aqi', 0)),
                'pm25': float(city.get('pm25', 0)),
                'crime_rate': float(city.get('crime_rate', 0)),
                'congestion_index': float(city.get('congestion_index', 0)),
                'rent_affordability': float(city.get('rent_affordability', 0)),
                'literacy_rate': float(city.get('literacy_rate', 0))
            }
        }

    def get_anomaly_report(self) -> Dict:
        """
        Detect outliers across key metrics using z-score thresholds.
        """
        if self.rankings is None:
            raise ValueError("No rankings available. Run pipeline first.")

        df = self.rankings.copy()
        metrics = [
            "livability_score",
            "aqi",
            "crime_rate",
            "congestion_index",
            "rent_affordability",
        ]

        report = {}
        for metric in metrics:
            if metric not in df.columns:
                continue
            values = df[metric].astype(float)
            std = float(values.std() or 0)
            if std == 0:
                continue
            mean = float(values.mean())
            z_scores = (values - mean) / std

            high = df[z_scores >= 1.5].sort_values(metric, ascending=False)
            low = df[z_scores <= -1.5].sort_values(metric, ascending=True)

            report[metric] = {
                "mean": mean,
                "std": std,
                "high_outliers": high[["city_name", "state", metric]].head(5).to_dict("records"),
                "low_outliers": low[["city_name", "state", metric]].head(5).to_dict("records"),
            }

        return report

    def get_report_payload(self) -> Dict:
        """
        Build a lightweight report payload for exports.
        """
        if self.rankings is None:
            raise ValueError("No rankings available. Run pipeline first.")

        return {
            "summary": {
                "cities": int(len(self.rankings)),
                "top_city": self.rankings.iloc[0]["city_name"],
                "bottom_city": self.rankings.iloc[-1]["city_name"],
                "avg_score": float(self.rankings["livability_score"].mean()),
            },
            "top_10": self.rankings.head(10).to_dict("records"),
            "bottom_10": self.rankings.tail(10).to_dict("records"),
        }


# Global service instance
_service_instance = None


def get_data_service() -> DataProcessingService:
    """Get or create the global data processing service"""
    global _service_instance
    if _service_instance is None:
        _service_instance = DataProcessingService()
    return _service_instance
