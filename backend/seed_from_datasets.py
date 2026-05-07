"""
Seed Supabase from the bundled dataset archive.

Run from the backend directory:
    python seed_from_datasets.py
"""

from __future__ import annotations

import os
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from dotenv import load_dotenv

backend_dir = Path(__file__).parent
project_root = backend_dir.parent
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

load_dotenv(backend_dir / ".env.local", override=True)

from database import Base, SessionLocal, engine
from models import CategoryScore, City, LivabilityScore, RawMetric

DATASET_ARCHIVE = Path(os.getenv("DATASET_ARCHIVE_PATH", project_root / "Datasets.zip"))
RESET_DATABASE = os.getenv("RESET_DATABASE", "true").lower() in {"1", "true", "yes", "on"}

CITY_ALIASES = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "new delhi": "Delhi",
    "delhi ncr": "Delhi",
    "bombay": "Mumbai",
}

TIER_ONE_CITIES = {
    "Ahmedabad",
    "Bengaluru",
    "Chennai",
    "Delhi",
    "Hyderabad",
    "Kolkata",
    "Mumbai",
    "Pune",
    "Surat",
}

SHEET_SPECS: dict[str, dict[str, str]] = {
    "Datasets/Cost_of_Living_Dataset.xlsx": {
        "avg_house_rent": "Avg House Rent (₹)",
        "utility_bills": "Utility Bills (₹)",
        "monthly_living_cost": "Monthly Living Cost (₹)",
    },
    "Datasets/Crime_Dataset.xlsx": {
        "theft_cases": "Theft Cases (Approx)",
        "violent_crime_cases": "Violent Crime Cases",
        "women_safety_complaints": "Women Safety Complaints",
        "crime_rate_per_lakh": "Crime Rate per Lakh",
    },
    "Datasets/education_facilities_dataset.xlsx": {
        "state": "State",
        "number_schools": "Number of Schools",
        "colleges_universities": "Colleges/Universities",
        "literacy_rate_pct": "Literacy Rate (%)",
    },
    "Datasets/healthcare_facilities_dataset.xlsx": {
        "state": "State",
        "number_hospitals": "Number of Hospitals",
        "beds_per_lakh_population": "Beds per Lakh Population",
    },
    "Datasets/pollution_dataset.xlsx": {
        "state": "State",
        "aqi_avg": "AQI (Avg)",
        "pm25": "PM2.5 (µg/m³)",
        "pm10": "PM10 (µg/m³)",
        "industrial_pollution": "Industrial Pollution (1-10)",
        "waste_generation": "Waste Generation (tons/day)",
    },
    "Datasets/Population_Density_Dataset.xlsx": {
        "state": "State",
        "population_density": "Population Density (per km²)",
        "urban_crowding_level": "Urban Crowding Level (1-5)",
    },
    "Datasets/Public_Transport_Dataset.xlsx": {
        "bus_availability": "Bus Availability (1-5)",
        "metro_train_connectivity": "Metro/Train Connectivity (1-5)",
        "coverage_area": "Coverage Area (1-5)",
    },
    "Datasets/sewerage_sanitation_dataset.xlsx": {
        "state": "State",
        "sewerage_coverage": "Sewerage Coverage (%)",
        "drainage_condition": "Drainage Condition (1-5)",
        "cleanliness_rating": "Cleanliness Rating (1-5)",
    },
    "Datasets/traffic_conditions_dataset.xlsx": {
        "state": "State",
        "traffic_congestion": "Traffic Congestion Level (1-10)",
        "peak_hour_traffic_load": "Peak-hour Traffic Load (1-10)",
        "road_accident_frequency": "Road Accident Frequency (per year)",
    },
    "Datasets/water_availability_dataset.xlsx": {
        "groundwater_level": "Groundwater Level (m)",
        "water_complaints": "Water Complaints (Annual)",
        "water_quality_index": "Water Quality Index (0-100)",
    },
}


def city_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def canonical_city_name(value: Any) -> str:
    key = city_key(value)
    return CITY_ALIASES.get(key, str(value).strip())


def infer_tier(city_name: str) -> str:
    return "Tier-1" if city_name in TIER_ONE_CITIES else "Tier-2"


def safe_float(value: Any) -> float | None:
    if pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# Scoring configuration and helpers (aligned with the notebook)
SCORING_CONFIG = {
    "method": "percentile",  # "percentile" | "minmax" | "benchmark"
    "score_floor": 10.0,
    "score_ceiling": 100.0,
}

BENCHMARK_RULES = {
    "aqi_avg": {
        "bins": [-np.inf, 50, 100, 200, 300, np.inf],
        "scores": [100, 85, 60, 35, 10],
    },
    "pm25": {
        "bins": [-np.inf, 30, 60, 90, 120, np.inf],
        "scores": [100, 85, 60, 35, 10],
    },
    "literacy_rate_pct": {
        "bins": [-np.inf, 60, 70, 80, 90, np.inf],
        "scores": [20, 40, 60, 80, 95],
    },
}


def minmax_score(series: pd.Series, positive: bool = True, floor: float = 0.0, ceiling: float = 100.0) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    mn, mx = s.min(skipna=True), s.max(skipna=True)

    if pd.isna(mn) or pd.isna(mx):
        return pd.Series(np.nan, index=s.index)
    if mx == mn:
        return pd.Series((floor + ceiling) / 2.0, index=s.index)

    if positive:
        base = (s - mn) / (mx - mn)
    else:
        base = (mx - s) / (mx - mn)

    score = floor + base * (ceiling - floor)
    return score.clip(floor, ceiling)


def percentile_score(series: pd.Series, positive: bool = True, floor: float = 10.0, ceiling: float = 100.0) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    valid = s.dropna()

    if valid.empty:
        return pd.Series(np.nan, index=s.index)

    n = len(valid)
    if n == 1:
        return pd.Series((floor + ceiling) / 2.0, index=s.index)

    pct = s.rank(method="average", pct=True, ascending=positive)
    min_pct = 1.0 / n
    base = (pct - min_pct) / (1.0 - min_pct)
    score = floor + base * (ceiling - floor)
    return score.clip(floor, ceiling)


def benchmark_score(series: pd.Series, subparam_name: str, floor: float, ceiling: float) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    rule = BENCHMARK_RULES.get(subparam_name)
    if rule is None:
        return percentile_score(s, positive=True, floor=floor, ceiling=ceiling)

    bins = rule["bins"]
    scores = rule["scores"]
    if len(scores) != len(bins) - 1:
        raise ValueError(f"Invalid benchmark rule for {subparam_name}: scores must be len(bins)-1")

    out = pd.cut(s, bins=bins, labels=False, include_lowest=True)
    mapped = out.map(lambda i: scores[int(i)] if pd.notna(i) else np.nan).astype(float)
    return mapped.clip(floor, ceiling)


def normalize_metric(series: pd.Series, positive: bool, config: dict, subparam_name: str) -> pd.Series:
    method = config.get("method", "percentile").lower()
    floor = float(config.get("score_floor", 0.0))
    ceiling = float(config.get("score_ceiling", 100.0))

    if method == "minmax":
        return minmax_score(series, positive=positive, floor=floor, ceiling=ceiling)
    if method == "percentile":
        return percentile_score(series, positive=positive, floor=floor, ceiling=ceiling)
    if method == "benchmark":
        return benchmark_score(series, subparam_name=subparam_name, floor=floor, ceiling=ceiling)
    raise ValueError(f"Unsupported scoring method: {method}")


# Category weights and sub-parameter config aligned with the notebook.
CATEGORY_WEIGHTS = {
    "crime": 0.15,
    "water": 0.12,
    "pollution": 0.10,
    "traffic": 0.10,
    "population": 0.06,
    "sanitation": 0.10,
    "education": 0.10,
    "healthcare": 0.12,
    "cost": 0.10,
    "transport": 0.05,
}

SUBPARAM_CONFIG = {
    "crime": {
        "subparams": {
            "theft_cases": {"weight": 0.20, "positive": False},
            "violent_crime_cases": {"weight": 0.35, "positive": False},
            "women_safety_complaints": {"weight": 0.25, "positive": False},
            "crime_rate_per_lakh": {"weight": 0.20, "positive": False},
        }
    },
    "water": {
        "subparams": {
            "groundwater_level": {"weight": 0.35, "positive": True},
            "water_complaints": {"weight": 0.30, "positive": False},
            "water_quality_index": {"weight": 0.35, "positive": True},
        }
    },
    "pollution": {
        "subparams": {
            "aqi_avg": {"weight": 0.40, "positive": False},
            "pm25": {"weight": 0.25, "positive": False},
            "pm10": {"weight": 0.20, "positive": False},
            "industrial_pollution": {"weight": 0.10, "positive": False},
            "waste_generation": {"weight": 0.05, "positive": False},
        }
    },
    "traffic": {
        "subparams": {
            "traffic_congestion": {"weight": 0.40, "positive": False},
            "peak_hour_traffic_load": {"weight": 0.30, "positive": False},
            "road_accident_frequency": {"weight": 0.30, "positive": False},
        }
    },
    "population": {
        "subparams": {
            "population_density": {"weight": 0.65, "positive": False},
            "urban_crowding_level": {"weight": 0.35, "positive": False},
        }
    },
    "sanitation": {
        "subparams": {
            "sewerage_coverage": {"weight": 0.40, "positive": True},
            "drainage_condition": {"weight": 0.30, "positive": True},
            "cleanliness_rating": {"weight": 0.30, "positive": True},
        }
    },
    "education": {
        "subparams": {
            "number_schools": {"weight": 0.25, "positive": True},
            "colleges_universities": {"weight": 0.25, "positive": True},
            "literacy_rate_pct": {"weight": 0.50, "positive": True},
        }
    },
    "healthcare": {
        "subparams": {
            "number_hospitals": {"weight": 0.40, "positive": True},
            "beds_per_lakh_population": {"weight": 0.60, "positive": True},
        }
    },
    "cost": {
        "subparams": {
            "avg_house_rent": {"weight": 0.40, "positive": False},
            "utility_bills": {"weight": 0.25, "positive": False},
            "monthly_living_cost": {"weight": 0.35, "positive": False},
        }
    },
    "transport": {
        "subparams": {
            "bus_availability": {"weight": 0.35, "positive": True},
            "metro_train_connectivity": {"weight": 0.40, "positive": True},
            "coverage_area": {"weight": 0.25, "positive": True},
        }
    },
}


def weighted_category_score(norm_df: pd.DataFrame, subparam_cfg: dict) -> pd.DataFrame:
    temp = norm_df.copy()
    cols_present = [c for c in subparam_cfg.keys() if c in temp.columns]

    if not cols_present:
        out = temp[["city"]].copy() if "city" in temp.columns else pd.DataFrame(index=temp.index)
        out = out.copy()
        out["score"] = np.nan
        return out

    weights = pd.Series({k: subparam_cfg[k]["weight"] for k in cols_present}, dtype=float)
    weights = weights / weights.sum()

    vals = temp[cols_present].apply(pd.to_numeric, errors="coerce")
    weighted_sum = vals.mul(weights, axis=1).sum(axis=1, skipna=True)
    available_weight = vals.notna().mul(weights, axis=1).sum(axis=1)
    score = weighted_sum.div(available_weight.where(available_weight > 0, np.nan))

    out = temp[["city"]].copy() if "city" in temp.columns else pd.DataFrame(index=temp.index)
    out["score"] = score
    return out


def read_sheet(archive: zipfile.ZipFile, member: str) -> pd.DataFrame:
    with archive.open(member) as file_handle:
        return pd.read_excel(file_handle, engine="openpyxl")


def build_master_frame() -> pd.DataFrame:
    if not DATASET_ARCHIVE.exists():
        raise FileNotFoundError(f"Dataset archive not found: {DATASET_ARCHIVE}")

    records: dict[str, dict[str, Any]] = {}

    with zipfile.ZipFile(DATASET_ARCHIVE) as archive:
        for member, rename_map in SHEET_SPECS.items():
            frame = read_sheet(archive, member)
            frame = frame.rename(columns=rename_map)

            for _, row in frame.iterrows():
                key = city_key(row["City"])
                record = records.setdefault(
                    key,
                    {
                        "city_name": canonical_city_name(row["City"]),
                        "state": None,
                    },
                )

                if "State" in row and not pd.isna(row["State"]):
                    record["state"] = str(row["State"]).strip()

                for column_name, source_name in rename_map.items():
                    if column_name == "state" or source_name == "State":
                        continue
                    record[column_name] = safe_float(row.get(source_name))

    frame = pd.DataFrame(records.values())
    frame = frame.sort_values("city_name").reset_index(drop=True)
    frame["state"] = frame["state"].fillna("Unknown")
    frame["tier"] = frame["city_name"].map(infer_tier)
    return frame


def clear_existing_data(db) -> None:
    db.query(LivabilityScore).delete()
    db.query(CategoryScore).delete()
    db.query(RawMetric).delete()
    db.query(City).delete()
    db.commit()


def insert_cities(db, frame: pd.DataFrame) -> dict[str, City]:
    city_lookup: dict[str, City] = {}
    for _, row in frame.iterrows():
        city = City(
            city_name=row["city_name"],
            state=row["state"],
            latitude=None,
            longitude=None,
            population=None,
            tier=row["tier"],
        )
        db.add(city)
        db.flush()
        city_lookup[row["city_name"]] = city
    db.commit()
    return city_lookup


def populate_raw_metrics(db, frame: pd.DataFrame, city_lookup: dict[str, City]) -> None:
    for _, row in frame.iterrows():
        db.add(
            RawMetric(
                city_id=city_lookup[row["city_name"]].id,
                aqi=row.get("aqi_avg"),
                pm25=row.get("pm25"),
                pm10=row.get("pm10"),
                congestion_index=row.get("traffic_congestion"),
                rent_affordability=row.get("monthly_living_cost"),
                crime_rate=row.get("crime_rate_per_lakh"),
                literacy_rate=row.get("literacy_rate_pct"),
                healthcare_facilities=row.get("number_hospitals"),
            )
        )
    db.commit()


def populate_category_scores(db, frame: pd.DataFrame, city_lookup: dict[str, City]) -> None:
    # Build a norm_df per category using SUBPARAM_CONFIG and SCORING_CONFIG
    category_scores_by_city: dict[str, dict[str, float]] = {name: {} for name in frame["city_name"]}

    for category, cfg in SUBPARAM_CONFIG.items():
        subparams = cfg["subparams"]
        cols_present = [c for c in subparams.keys() if c in frame.columns]
        if not cols_present:
            continue

        norm_table = pd.DataFrame({"city": frame["city_name"]})
        for col in cols_present:
            positive = subparams[col]["positive"]
            norm_table[col] = normalize_metric(frame[col], positive=positive, config=SCORING_CONFIG, subparam_name=col)

        scored = weighted_category_score(norm_table, {k: subparams[k] for k in cols_present})
        score_col = f"{category}_score"

        # insert (or store) the category score values
        for idx, row in scored.reset_index(drop=True).iterrows():
            city = row["city"]
            val = float(row["score"]) if pd.notna(row["score"]) else None
            category_scores_by_city[city][score_col] = val

    # Write CategoryScore rows using city_lookup
    for city_name, scores in category_scores_by_city.items():
        city_obj = city_lookup.get(city_name)
        if city_obj is None:
            continue

        cs = CategoryScore(
            city_id=city_obj.id,
            crime_score=scores.get("crime_score"),
            healthcare_score=scores.get("healthcare_score"),
            water_score=scores.get("water_score"),
            education_score=scores.get("education_score"),
            sanitation_score=scores.get("sanitation_score"),
            pollution_score=scores.get("pollution_score"),
            traffic_score=scores.get("traffic_score"),
            cost_score=scores.get("cost_score"),
            population_score=scores.get("population_score"),
            transport_score=scores.get("transport_score"),
        )
        db.add(cs)
    db.commit()


def populate_livability_scores(db, frame: pd.DataFrame, city_lookup: dict[str, City]) -> None:
    # Read category_scores back into a DataFrame for median-filling and weighted aggregation
    cats = db.query(CategoryScore).all()
    rows = []
    for c in cats:
        rows.append(
            {
                "city_id": c.city_id,
                "crime_score": c.crime_score,
                "healthcare_score": c.healthcare_score,
                "water_score": c.water_score,
                "education_score": c.education_score,
                "sanitation_score": c.sanitation_score,
                "pollution_score": c.pollution_score,
                "traffic_score": c.traffic_score,
                "cost_score": c.cost_score,
                "population_score": c.population_score,
                "transport_score": c.transport_score,
            }
        )

    cat_df = pd.DataFrame(rows)
    if cat_df.empty:
        return

    # Fill missing per-category with median
    for col in [f"{cat}_score" for cat in CATEGORY_WEIGHTS.keys()]:
        if col not in cat_df.columns:
            cat_df[col] = np.nan
        med = cat_df[col].median(skipna=True)
        if pd.isna(med):
            med = 50.0
        cat_df[col] = cat_df[col].fillna(med)

    # Compute weighted final score
    weight_items = [(f"{k}_score", v) for k, v in CATEGORY_WEIGHTS.items()]
    score_series = pd.Series(0.0, index=cat_df.index)
    for col, w in weight_items:
        score_series = score_series + cat_df[col] * w

    cat_df["overall_score"] = score_series

    ranking_rows = []
    for _, r in cat_df.iterrows():
        ranking_rows.append({"city_id": int(r["city_id"]), "overall_score": float(r["overall_score"])})

    ranking_rows.sort(key=lambda item: item["overall_score"], reverse=True)
    total_rows = len(ranking_rows)

    for rank, item in enumerate(ranking_rows, start=1):
        percentile = round(100 - (((rank - 1) / max(total_rows - 1, 1)) * 100), 2)
        db.add(
            LivabilityScore(
                city_id=item["city_id"],
                overall_score=item["overall_score"],
                rank=rank,
                percentile=percentile,
            )
        )
    db.commit()


def main() -> int:
    print("\n" + "=" * 72)
    print("  SUPABASE DATASET SEEDER")
    print("=" * 72)
    print(f"Dataset archive: {DATASET_ARCHIVE}")

    frame = build_master_frame()
    print(f"Loaded {len(frame)} cities from the bundled dataset archive.")

    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        if RESET_DATABASE:
            clear_existing_data(db)

        city_lookup = insert_cities(db, frame)
        populate_raw_metrics(db, frame, city_lookup)
        populate_category_scores(db, frame, city_lookup)
        populate_livability_scores(db, frame, city_lookup)

        print("\nSeed summary:")
        print(f"  Cities:            {db.query(City).count()}")
        print(f"  Raw Metrics:       {db.query(RawMetric).count()}")
        print(f"  Category Scores:    {db.query(CategoryScore).count()}")
        print(f"  Livability Scores:  {db.query(LivabilityScore).count()}")
        print("=" * 72 + "\n")
        return 0
    except Exception as exc:
        db.rollback()
        print(f"\n✗ Seeding failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
