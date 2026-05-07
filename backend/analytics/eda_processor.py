"""
EDA Processor for UrbanPulse IQ

Handles Exploratory Data Analysis transformations and insights generation.
Processes raw metrics and generates research-backed insights.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class InsightType(Enum):
    """Types of insights that can be generated"""
    POSITIVE = "positive"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Insight:
    """Data class for insights"""
    title: str
    description: str
    insight_type: InsightType
    confidence: float = 0.0


class EDAProcessor:
    """
    Performs EDA transformations and generates insights.
    """

    def __init__(self):
        """Initialize EDA processor"""
        self.data = None
        self.insights = []

    def load_data(self, df: pd.DataFrame):
        """Load data for analysis"""
        self.data = df.copy()

    def calculate_correlation_matrix(
        self,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Calculate Pearson correlation matrix
        
        Args:
            columns: Specific columns to correlate (None = all numeric)
        
        Returns:
            Correlation matrix
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        if columns:
            return self.data[columns].corr(method='pearson')
        else:
            return self.data.select_dtypes(include=[np.number]).corr()

    def calculate_spearman_correlation(
        self,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Calculate Spearman correlation matrix (rank-based)
        
        Args:
            columns: Specific columns to correlate
        
        Returns:
            Spearman correlation matrix
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        if columns:
            return self.data[columns].corr(method='spearman')
        else:
            return self.data.select_dtypes(include=[np.number]).corr(method='spearman')

    def detect_outliers(
        self,
        column: str,
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> List[int]:
        """
        Detect outliers in a column
        
        Args:
            column: Column name
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier (iqr) or z-score threshold
        
        Returns:
            List of outlier indices
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        data = self.data[column].dropna()
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            outliers = self.data[(self.data[column] < lower) | 
                                (self.data[column] > upper)].index.tolist()
        
        elif method == 'zscore':
            z_scores = np.abs((data - data.mean()) / data.std())
            outliers = self.data[np.abs((self.data[column] - data.mean()) / 
                                       data.std()) > threshold].index.tolist()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return outliers

    def identify_pollution_clusters(
        self,
        pollution_column: str,
        high_threshold: float = 150
    ) -> Dict[str, List[str]]:
        """
        Identify cities with pollution issues
        
        Args:
            pollution_column: Column name for pollution metric
            high_threshold: Threshold for high pollution
        
        Returns:
            Dictionary with pollution categories
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        high_pollution = self.data[self.data[pollution_column] > high_threshold]['city_name'].tolist()
        
        return {
            'high_pollution_cities': high_pollution,
            'count': len(high_pollution),
            'percentage': len(high_pollution) / len(self.data) * 100
        }

    def analyze_crime_population_relationship(
        self,
        crime_column: str,
        population_column: str
    ) -> Dict:
        """
        Analyze relationship between crime and population
        
        Args:
            crime_column: Column name for crime metric
            population_column: Column name for population
        
        Returns:
            Analysis results
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        if crime_column not in self.data.columns or population_column not in self.data.columns:
            return {'error': 'Required columns not found'}
        
        # Remove NaN values
        valid_data = self.data[[crime_column, population_column]].dropna()
        
        correlation = valid_data[crime_column].corr(valid_data[population_column])
        
        # Calculate per capita crime
        valid_data['crime_per_capita'] = valid_data[crime_column] / valid_data[population_column]
        
        return {
            'correlation': correlation,
            'crime_population_relationship': 'strong' if abs(correlation) > 0.7 else 'moderate' if abs(correlation) > 0.4 else 'weak',
            'cities_with_scaling_crime': valid_data.nlargest(5, 'crime_per_capita').index.tolist()
        }

    def analyze_cost_livability_relationship(
        self,
        cost_column: str,
        livability_column: str
    ) -> Dict:
        """
        Analyze relationship between cost and livability
        
        Args:
            cost_column: Column name for cost metric
            livability_column: Column name for livability score
        
        Returns:
            Analysis results
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        valid_data = self.data[[cost_column, livability_column]].dropna()
        
        correlation = valid_data[cost_column].corr(valid_data[livability_column])
        
        # Identify cost outliers
        cost_mean = valid_data[cost_column].mean()
        cost_std = valid_data[cost_column].std()
        
        expensive_cities = self.data[
            self.data[cost_column] > (cost_mean + 2 * cost_std)
        ]['city_name'].tolist()
        
        return {
            'correlation': correlation,
            'insight': 'High cost negatively impacts livability' if correlation < -0.3 else 'Cost does not significantly impact livability',
            'expensive_outliers': expensive_cities
        }

    def analyze_tier_performance(
        self,
        tier_column: str,
        score_column: str
    ) -> Dict:
        """
        Analyze livability performance by city tier
        
        Args:
            tier_column: Column name for city tier
            score_column: Column name for livability score
        
        Returns:
            Tier performance analysis
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        tier_stats = self.data.groupby(tier_column)[score_column].agg([
            'mean', 'median', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        tier_performance = {}
        for tier in tier_stats.index:
            tier_performance[tier] = {
                'mean_score': float(tier_stats.loc[tier, 'mean']),
                'median_score': float(tier_stats.loc[tier, 'median']),
                'std_dev': float(tier_stats.loc[tier, 'std']),
                'city_count': int(tier_stats.loc[tier, 'count'])
            }
        
        return tier_performance

    def generate_city_insights(
        self,
        city_name: str,
        scores: Dict[str, float]
    ) -> List[Insight]:
        """
        Generate insights for a specific city
        
        Args:
            city_name: Name of city
            scores: Dictionary of category scores
        
        Returns:
            List of Insight objects
        """
        insights = []
        
        # Strength/weakness insights
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        top_strength = sorted_scores[0]
        bottom_weakness = sorted_scores[-1]
        
        if top_strength[1] > 80:
            insights.append(Insight(
                title=f"Strong {top_strength[0].replace('_', ' ').title()}",
                description=f"{city_name} excels in {top_strength[0].replace('_', ' ')} with a score of {top_strength[1]:.1f}",
                insight_type=InsightType.POSITIVE,
                confidence=0.95
            ))
        
        if bottom_weakness[1] < 40:
            insights.append(Insight(
                title=f"Critical {bottom_weakness[0].replace('_', ' ').title()} Issues",
                description=f"{city_name} needs improvement in {bottom_weakness[0].replace('_', ' ')} (score: {bottom_weakness[1]:.1f})",
                insight_type=InsightType.CRITICAL,
                confidence=0.90
            ))
        
        return insights

    def generate_research_insights(self, df: pd.DataFrame) -> List[Insight]:
        """
        Generate research-backed insights from data
        
        Args:
            df: DataFrame with city data
        
        Returns:
            List of research insights
        """
        self.load_data(df)
        insights = []
        
        # Insight 1: Tier-2 Performance
        if 'tier' in df.columns and 'livability_score' in df.columns:
            tier2_mean = df[df['tier'] == 'Tier-2']['livability_score'].mean()
            tier1_mean = df[df['tier'] == 'Tier-1']['livability_score'].mean()
            
            if tier2_mean > tier1_mean:
                insights.append(Insight(
                    title="Tier-2 City Outperformance",
                    description="Tier-2 cities outperform Tier-1 metros in balanced livability metrics",
                    insight_type=InsightType.POSITIVE,
                    confidence=0.85
                ))
        
        # Insight 2: Pollution Burden
        if 'pm25' in df.columns:
            high_pollution_count = len(df[df['pm25'] > 150])
            if high_pollution_count > 0:
                insights.append(Insight(
                    title="Northern Pollution Burden",
                    description=f"{high_pollution_count} cities exhibit elevated pollution levels impacting livability",
                    insight_type=InsightType.CRITICAL,
                    confidence=0.90
                ))
        
        # Insight 3: Traffic Impact
        if 'congestion_index' in df.columns and 'livability_score' in df.columns:
            correlation = df['congestion_index'].corr(df['livability_score'])
            if correlation < -0.6:
                insights.append(Insight(
                    title="Traffic Congestion Impact",
                    description="Traffic congestion strongly correlates with livability decline",
                    insight_type=InsightType.WARNING,
                    confidence=0.88
                ))
        
        return insights
