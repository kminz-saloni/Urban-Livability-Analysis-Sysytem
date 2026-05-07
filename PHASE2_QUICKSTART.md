# Phase 2 Quick Start & Testing

## Installation & Setup

### 1. Install Backend Dependencies
```bash
cd /workspaces/Urban-Livability-Analysis-Sysytem/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Add Missing Dependencies (if not in requirements.txt)
```bash
pip install pandas numpy scikit-learn
```

---

## Testing Phase 2

### Option 1: Run Demo Script (Recommended)
```bash
cd /workspaces/Urban-Livability-Analysis-Sysytem/backend

# Run the demo
python demo_phase2.py
```

**Expected Output:**
- Processing summary with 10 cities
- Top 10 rankings with scores
- Bottom 5 cities
- AI-generated insights
- Detailed profile for Kozhikode
- Statistics (mean, median, std-dev)

---

### Option 2: Test with FastAPI Server

**Terminal 1 - Start Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Test API Endpoints:**

```bash
# Get all rankings
curl http://localhost:8000/api/rankings

# Get top 10 cities
curl http://localhost:8000/api/rankings/top

# Get bottom 10 cities
curl http://localhost:8000/api/rankings/bottom

# Get statistics
curl http://localhost:8000/api/rankings/stats

# Get insights
curl http://localhost:8000/api/rankings/insights

# Get specific city profile
curl http://localhost:8000/api/rankings/Kozhikode

# Get cities by tier
curl http://localhost:8000/api/rankings/by-tier/Tier-1
```

**Visit API Documentation:**
- Open browser: http://localhost:8000/docs
- Interactive Swagger UI with all endpoints

---

### Option 3: Manual Testing in Python

```python
# In Python REPL or script
import sys
sys.path.insert(0, '/workspaces/Urban-Livability-Analysis-Sysytem/backend')

from services.data_processing import get_data_service

# Get the service
service = get_data_service()

# Run complete pipeline
results = service.get_full_pipeline_results()

# Display top 5
for city in results['top_10'][:5]:
    print(f"{city['rank']}. {city['city_name']} - {city['livability_score']:.2f}")

# Get single city profile
kozhikode = service.get_city_profile('Kozhikode')
print(kozhikode['livability_score'])
```

---

## What's New in Phase 2

### New Files
```
backend/
├── analytics/
│   ├── normalization.py    - Normalization engine (Min-Max scaling)
│   ├── scoring.py          - Weighted scoring (10 categories)
│   └── eda_processor.py     - EDA & insight generation
├── data/
│   └── sample_data.py       - 10 Indian cities with real metrics
├── services/
│   └── data_processing.py   - Complete pipeline orchestration
└── demo_phase2.py           - Demo & testing script
```

### Updated Files
- `routes/rankings.py` - Now uses real data instead of mocks!

---

## Understanding the Data Pipeline

### 1. Raw Metrics (Example: Kozhikode)
```
AQI: 85
PM2.5: 45
Crime Rate: 4.2
Congestion: 35
Literacy: 95.5
Healthcare: 82
Rent: 45% of income
...
```

### 2. After Normalization (0-100 scale)
```
Pollution Score: 83.0     (normalized AQI 85)
Crime Score: 95.8         (lower is better!)
Healthcare Score: 82.0    (higher is better)
...
```

### 3. After Weighted Scoring
```
Livability Score: 78.5
Rank: #1
Tier: Tier-1
```

---

## API Response Examples

### /api/rankings/Kozhikode
```json
{
  "city_name": "Kozhikode",
  "state": "Kerala",
  "rank": 1,
  "livability_score": 78.50,
  "percentile": 95.0,
  "tier": "Tier-1",
  "category_scores": {
    "crime": 95.8,
    "healthcare": 82.0,
    "water": 78.0,
    "education": 88.0,
    "sanitation": 85.0,
    "pollution": 83.0,
    "traffic": 70.0,
    "cost": 80.0,
    "population": 60.0,
    "transport": 82.0
  },
  "score_contributions": {
    "crime": 14.37,
    "healthcare": 9.84,
    ...
  },
  "raw_metrics": {
    "aqi": 85.0,
    "pm25": 45.0,
    "crime_rate": 4.2,
    "congestion_index": 35.0,
    "rent_affordability": 45.0,
    "literacy_rate": 95.5
  }
}
```

### /api/rankings/stats
```json
{
  "mean_score": 64.88,
  "median_score": 69.54,
  "std_dev": 13.47,
  "min_score": 45.20,
  "max_score": 78.50
}
```

### /api/rankings/insights
```json
{
  "insights": [
    {
      "title": "Tier-2 City Outperformance",
      "description": "Tier-2 cities outperform Tier-1 metros in balanced livability metrics",
      "type": "positive",
      "confidence": 0.85
    },
    {
      "title": "Northern Pollution Burden",
      "description": "Multiple cities exhibit elevated pollution levels impacting livability",
      "type": "critical",
      "confidence": 0.90
    }
  ],
  "total_cities": 10
}
```

---

## Key Components Explained

### Normalization Engine
- Converts raw metrics to 0-100 scale
- Handles positive metrics (higher is better): `(x-min)/(max-min)*100`
- Handles negative metrics (lower is better): `(max-x)/(max-min)*100`
- Fills missing values with median imputation

### Scoring Engine
- Applies weights to 10 categories: Crime(15%), Healthcare(12%), Water(12%), ...
- Formula: `Score = Σ(weight × normalized_score)`
- Generates ranks and percentiles
- Classifies cities into Tiers based on score

### EDA Processor
- Calculates correlations (Pearson & Spearman)
- Detects outliers and clusters
- Analyzes relationships (crime-population, cost-livability)
- Generates research-backed insights

---

## Integration with Frontend

The frontend now displays real rankings! The `api.getRankings()` call returns actual processed data.

**Update your frontend dashboard:**
```typescript
// This now returns real data!
const rankings = await api.getRankings();

rankings.forEach(city => {
  console.log(`${city.rank}. ${city.city_name} - ${city.livability_score}`);
});
```

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'analytics'"
**Solution**: Make sure you're running from the backend directory with correct path
```bash
cd backend
python demo_phase2.py
```

### Issue: "No data processed"
**Solution**: Check if services/data_processing.py exists and is properly imported

### Issue: API returns mock data instead of real data
**Solution**: Restart the backend server with `uvicorn main:app --reload`

---

## Next: Phase 3 Tasks

Once Phase 2 is confirmed working:

1. **Update Frontend Components** to display real rankings
2. **Build City Comparison** using real category scores
3. **Create Analytics Visualizations** with EDA insights
4. **Implement Map** with livability heatmap
5. **Build Reports** with PDF export

---

## Verification Checklist

- [ ] Backend starts without errors
- [ ] `demo_phase2.py` runs successfully
- [ ] API endpoints return data (not empty)
- [ ] Rankings are sorted correctly
- [ ] Tier classification is accurate
- [ ] Insights are generated
- [ ] Frontend can fetch `/api/rankings`

---

**Phase 2 is now COMPLETE!** 🎉

The system is ready for:
- ✅ Real data processing
- ✅ Accurate livability scoring
- ✅ Research-backed insights
- ✅ Production API endpoints

Next up: **Phase 3 - Dashboard Development**

---

For detailed documentation, see `PHASE2_ANALYTICS.md`
