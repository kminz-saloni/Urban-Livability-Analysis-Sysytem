"""
Normalization Engine for UrbanPulse IQ

Handles Min-Max scaling and normalization of urban metrics.
Converts raw metrics to normalized 0-100 scale.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional


class NormalizationEngine:
    """
    Normalizes urban metrics using Min-Max scaling.
    Handles both positive and negative indicators.
    """

    def __init__(self):
        """Initialize the normalization engine"""
        self.scaler_stats = {}

    def normalize_positive_metric(
        self, 
        values: np.ndarray,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> np.ndarray:
        """
        Normalize positive indicator (higher is better)
        Formula: (x - min) / (max - min) * 100
        
        Args:
            values: Array of values to normalize
            min_val: Manual minimum value (optional)
            max_val: Manual maximum value (optional)
        
        Returns:
            Normalized array with values 0-100
        """
        values_array = np.array(values)
        
        min_val = min_val if min_val is not None else np.nanmin(values_array)
        max_val = max_val if max_val is not None else np.nanmax(values_array)
        
        if max_val == min_val:
            return np.full_like(values_array, 50.0, dtype=float)
        
        normalized = ((values_array - min_val) / (max_val - min_val)) * 100
        normalized = np.clip(normalized, 0, 100)
        
        return normalized

    def normalize_negative_metric(
        self,
        values: np.ndarray,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> np.ndarray:
        """
        Normalize negative indicator (lower is better)
        Formula: (max - x) / (max - min) * 100
        
        Args:
            values: Array of values to normalize
            min_val: Manual minimum value (optional)
            max_val: Manual maximum value (optional)
        
        Returns:
            Normalized array with values 0-100
        """
        values_array = np.array(values)
        
        min_val = min_val if min_val is not None else np.nanmin(values_array)
        max_val = max_val if max_val is not None else np.nanmax(values_array)
        
        if max_val == min_val:
            return np.full_like(values_array, 50.0, dtype=float)
        
        normalized = ((max_val - values_array) / (max_val - min_val)) * 100
        normalized = np.clip(normalized, 0, 100)
        
        return normalized

    def normalize_metric_by_scale(
        self,
        values: np.ndarray,
        metric_type: str,  # 'positive' or 'negative'
        bounds: Optional[Tuple[float, float]] = None
    ) -> np.ndarray:
        """
        Normalize metric with specified type and optional bounds
        
        Args:
            values: Array of values
            metric_type: 'positive' or 'negative'
            bounds: Tuple of (min, max) for scaling
        
        Returns:
            Normalized values 0-100
        """
        min_val, max_val = bounds if bounds else (None, None)
        
        if metric_type == 'positive':
            return self.normalize_positive_metric(values, min_val, max_val)
        elif metric_type == 'negative':
            return self.normalize_negative_metric(values, min_val, max_val)
        else:
            raise ValueError(f"Unknown metric type: {metric_type}")

    def handle_missing_values(
        self,
        values: List[Optional[float]],
        strategy: str = 'median'
    ) -> np.ndarray:
        """
        Handle missing values in data
        
        Args:
            values: List with potential None values
            strategy: 'median', 'mean', or 'zero'
        
        Returns:
            Array with missing values filled
        """
        arr = np.array([v if v is not None else np.nan for v in values])
        
        if strategy == 'median':
            fill_value = np.nanmedian(arr)
        elif strategy == 'mean':
            fill_value = np.nanmean(arr)
        elif strategy == 'zero':
            fill_value = 0
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        arr = np.nan_to_num(arr, nan=fill_value)
        return arr

    def standardize_column(
        self,
        values: np.ndarray,
        mean: Optional[float] = None,
        std: Optional[float] = None
    ) -> np.ndarray:
        """
        Standardize values to mean=0, std=1
        
        Args:
            values: Array to standardize
            mean: Manual mean (optional)
            std: Manual standard deviation (optional)
        
        Returns:
            Standardized array
        """
        values_array = np.array(values)
        mean = mean if mean is not None else np.nanmean(values_array)
        std = std if std is not None else np.nanstd(values_array)
        
        if std == 0:
            return np.zeros_like(values_array, dtype=float)
        
        return (values_array - mean) / std

    def percentile_rank(self, values: np.ndarray) -> np.ndarray:
        """
        Convert values to percentile ranks (0-100)
        
        Args:
            values: Array of values
        
        Returns:
            Percentile ranks
        """
        return np.array([100 * np.mean(values <= v) for v in values])


# Metric type definitions
METRIC_TYPES = {
    # Positive indicators (higher is better)
    'healthcare_score': 'positive',
    'literacy_rate': 'positive',
    'education_score': 'positive',
    'transport_facilities': 'positive',
    'airport_connectivity': 'positive',
    'wifi_coverage': 'positive',
    'green_space_ratio': 'positive',
    'sanitation_score': 'positive',
    
    # Negative indicators (lower is better)
    'aqi': 'negative',
    'pm25': 'negative',
    'pm10': 'negative',
    'crime_rate': 'negative',
    'crime_density': 'negative',
    'congestion_index': 'negative',
    'rent_affordability': 'negative',  # Higher rent = negative
    'pollution_level': 'negative',
    'water_contamination': 'negative',
    'groundwater_depletion': 'negative',
    'women_crime_rate': 'negative',
}

# Metric bounds (min, max) for normalization
METRIC_BOUNDS = {
    'aqi': (0, 500),
    'pm25': (0, 500),
    'pm10': (0, 500),
    'crime_rate': (0, 100),
    'congestion_index': (0, 100),
    'rent_affordability': (0, 100),
    'literacy_rate': (0, 100),
    'healthcare_score': (0, 100),
    'education_score': (0, 100),
    'sanitation_score': (0, 100),
}
