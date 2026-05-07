"""
Scoring Engine for UrbanPulse IQ

Implements weighted scoring model based on research-backed methodology.
Calculates overall livability scores and rankings.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import date


@dataclass
class WeightConfig:
    """Configuration for weighted scoring"""
    crime: float = 0.15
    healthcare: float = 0.12
    water: float = 0.12
    education: float = 0.10
    sanitation: float = 0.10
    pollution: float = 0.10
    traffic: float = 0.10
    cost: float = 0.10
    population: float = 0.06
    transport: float = 0.05

    def validate(self):
        """Ensure weights sum to 1.0"""
        total = sum([
            self.crime, self.healthcare, self.water, self.education,
            self.sanitation, self.pollution, self.traffic, self.cost,
            self.population, self.transport
        ])
        if not np.isclose(total, 1.0):
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            'crime': self.crime,
            'healthcare': self.healthcare,
            'water': self.water,
            'education': self.education,
            'sanitation': self.sanitation,
            'pollution': self.pollution,
            'traffic': self.traffic,
            'cost': self.cost,
            'population': self.population,
            'transport': self.transport,
        }


class ScoringEngine:
    """
    Calculates weighted livability scores for cities.
    
    Formula: L = Σ(w_i × x_i)
    where:
        L = Livability score
        w_i = category weight
        x_i = normalized category score (0-100)
    """

    def __init__(self, weight_config: Optional[WeightConfig] = None):
        """
        Initialize scoring engine
        
        Args:
            weight_config: WeightConfig object (uses defaults if not provided)
        """
        self.weights = weight_config or WeightConfig()
        self.weights.validate()

    def calculate_score(
        self,
        crime_score: float,
        healthcare_score: float,
        water_score: float,
        education_score: float,
        sanitation_score: float,
        pollution_score: float,
        traffic_score: float,
        cost_score: float,
        population_score: float,
        transport_score: float
    ) -> float:
        """
        Calculate weighted livability score
        
        Args:
            All category scores (0-100)
        
        Returns:
            Weighted livability score (0-100)
        """
        scores = [
            crime_score,
            healthcare_score,
            water_score,
            education_score,
            sanitation_score,
            pollution_score,
            traffic_score,
            cost_score,
            population_score,
            transport_score
        ]
        
        weights_list = [
            self.weights.crime,
            self.weights.healthcare,
            self.weights.water,
            self.weights.education,
            self.weights.sanitation,
            self.weights.pollution,
            self.weights.traffic,
            self.weights.cost,
            self.weights.population,
            self.weights.transport
        ]
        
        # Handle missing scores
        scores = [s if s is not None else 50 for s in scores]
        
        # Weighted sum
        weighted_score = sum(s * w for s, w in zip(scores, weights_list))
        
        return np.clip(weighted_score, 0, 100)

    def calculate_scores_batch(
        self,
        category_data: Dict[str, List[float]]
    ) -> List[float]:
        """
        Calculate scores for multiple cities
        
        Args:
            category_data: Dictionary with category names as keys,
                          lists of scores as values
        
        Returns:
            List of overall livability scores
        """
        required_categories = [
            'crime_score', 'healthcare_score', 'water_score',
            'education_score', 'sanitation_score', 'pollution_score',
            'traffic_score', 'cost_score', 'population_score',
            'transport_score'
        ]
        
        for cat in required_categories:
            if cat not in category_data:
                raise ValueError(f"Missing required category: {cat}")
        
        num_cities = len(category_data['crime_score'])
        scores = []
        
        for i in range(num_cities):
            score = self.calculate_score(
                crime_score=category_data['crime_score'][i],
                healthcare_score=category_data['healthcare_score'][i],
                water_score=category_data['water_score'][i],
                education_score=category_data['education_score'][i],
                sanitation_score=category_data['sanitation_score'][i],
                pollution_score=category_data['pollution_score'][i],
                traffic_score=category_data['traffic_score'][i],
                cost_score=category_data['cost_score'][i],
                population_score=category_data['population_score'][i],
                transport_score=category_data['transport_score'][i]
            )
            scores.append(score)
        
        return scores

    def rank_cities(
        self,
        city_names: List[str],
        scores: List[float]
    ) -> pd.DataFrame:
        """
        Generate ranking from scores
        
        Args:
            city_names: List of city names
            scores: List of livability scores
        
        Returns:
            DataFrame with ranks, city names, scores, percentiles
        """
        df = pd.DataFrame({
            'city_name': city_names,
            'livability_score': scores
        })
        
        df = df.sort_values('livability_score', ascending=False)
        df['rank'] = range(1, len(df) + 1)
        df['percentile'] = (df['rank'] - 1) / len(df) * 100
        
        return df.reset_index(drop=True)[['rank', 'city_name', 'livability_score', 'percentile']]

    def get_city_tier(self, score: float) -> str:
        """
        Classify city into tiers based on score
        
        Args:
            score: Livability score (0-100)
        
        Returns:
            Tier classification
        """
        if score >= 75:
            return "Tier-1"
        elif score >= 60:
            return "Tier-2"
        else:
            return "Tier-3"

    def calculate_score_contribution(
        self,
        crime_score: float,
        healthcare_score: float,
        water_score: float,
        education_score: float,
        sanitation_score: float,
        pollution_score: float,
        traffic_score: float,
        cost_score: float,
        population_score: float,
        transport_score: float
    ) -> Dict[str, float]:
        """
        Calculate individual category contributions to overall score
        
        Args:
            All category scores (0-100)
        
        Returns:
            Dictionary with category names and their contributions
        """
        scores = {
            'crime': crime_score,
            'healthcare': healthcare_score,
            'water': water_score,
            'education': education_score,
            'sanitation': sanitation_score,
            'pollution': pollution_score,
            'traffic': traffic_score,
            'cost': cost_score,
            'population': population_score,
            'transport': transport_score
        }
        
        weights_dict = self.weights.to_dict()
        
        contributions = {}
        for category, score in scores.items():
            score = score if score is not None else 50
            contribution = score * weights_dict[category]
            contributions[category] = contribution
        
        return contributions

    def get_strength_and_weaknesses(
        self,
        scores_dict: Dict[str, float],
        top_n: int = 3
    ) -> Tuple[List[str], List[str]]:
        """
        Identify top strengths and weaknesses for a city
        
        Args:
            scores_dict: Dictionary of category scores
            top_n: Number of strengths/weaknesses to return
        
        Returns:
            Tuple of (strengths, weaknesses) lists
        """
        sorted_cats = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
        
        strengths = [cat for cat, _ in sorted_cats[:top_n]]
        weaknesses = [cat for cat, _ in sorted_cats[-top_n:]]
        
        return strengths, weaknesses
