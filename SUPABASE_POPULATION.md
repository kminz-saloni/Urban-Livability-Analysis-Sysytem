# Supabase Database Population Guide

## Overview

The Urban Livability Analysis System uses Supabase PostgreSQL to store:
- City information
- Raw metrics (air quality, crime rates, etc.)
- Category scores (derived from raw metrics)
- Overall livability scores and rankings

## Option 1: Run Locally (Recommended First Time)

### Prerequisites
- Python 3.9+
- Virtual environment with dependencies installed

### Steps

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Ensure .env.local has correct DATABASE_URL:**
   ```bash
   cat .env.local
   ```
   Should show: `DATABASE_URL=postgresql://postgres:...@db.onwsdqfcisezshmvsmek.supabase.co:5432/postgres`

3. **Run population script:**
   ```bash
   python populate_database.py
   ```

4. **Expected output:**
   ```
   ======================================================================
     SUPABASE DATABASE POPULATION SCRIPT
   ======================================================================
   
   🔧 Creating database tables...
   ✓ Database tables created successfully
   
   📍 Populating cities...
     ✓ Added: Kozhikode, Kerala
     ✓ Added: Coimbatore, Tamil Nadu
     ...
   
   📊 Populating raw metrics...
   🎯 Populating category scores...
   ⭐ Populating livability scores...
   
   ======================================================================
     POPULATION SUMMARY
   ======================================================================
   
   ✓ Cities:            50+
   ✓ Raw Metrics:       50+
   ✓ Category Scores:   50+
   ✓ Livability Scores: 50+
   
   ======================================================================
     ✓ DATABASE POPULATION COMPLETE!
   ======================================================================
   ```

## Option 2: Run via Azure App Service SSH

If you have SSH access to the deployed backend:

```bash
# SSH into Azure App Service
ssh user@urban-backend.azurewebsites.net

# Navigate to app directory
cd /home/site/wwwroot

# Run population script
python populate_database.py
```

## Option 3: Add to Startup Script

To auto-populate on deployment, add to `backend/startup.sh`:

```bash
#!/bin/bash

# Create tables and populate data
python populate_database.py

# Start the application
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Verify Data in Supabase

1. **Go to Supabase Dashboard:**
   - URL: https://app.supabase.com
   - Project: Urban Livability Analysis

2. **Check tables:**
   - SQL Editor → Run queries:
     ```sql
     SELECT COUNT(*) FROM cities;
     SELECT COUNT(*) FROM livability_scores;
     SELECT COUNT(*) FROM category_scores;
     SELECT COUNT(*) FROM raw_metrics;
     ```

3. **View data:**
   ```sql
   SELECT c.city_name, ls.overall_score, ls.rank 
   FROM cities c
   JOIN livability_scores ls ON c.id = ls.city_id
   ORDER BY ls.rank
   LIMIT 10;
   ```

## Data Structure

### Cities Table
- `city_name`: Name of city
- `state`: State/Province
- `latitude`, `longitude`: Geographic coordinates
- `population`: City population
- `tier`: Tier-1, Tier-2, or Tier-3

### Raw Metrics Table
- Actual values: AQI, PM2.5, PM10, crime rate, congestion index, etc.

### Category Scores Table
- Normalized scores (0-100) for each category
- 10 categories: crime, healthcare, water, education, sanitation, pollution, traffic, cost, population, transport

### Livability Scores Table
- `overall_score`: Average of all category scores
- `rank`: Ranking among all cities
- `percentile`: Percentile ranking

## Troubleshooting

### "Could not open requirements file" error
```bash
# Make sure you're in the backend directory
cd backend
python populate_database.py
```

### "Connection refused" to Supabase
```bash
# Check .env.local has correct DATABASE_URL
cat .env.local 

# Test connection
psql postgresql://postgres:PASSWORD@db.onwsdqfcisezshmvsmek.supabase.co:5432/postgres
```

### "Table already exists" error
- This is normal if running the script twice
- The script checks for existing data and skips duplicates
- To reset: Use Supabase dashboard to truncate tables

## Frontend API Testing

After population, verify the backend API:

```bash
curl https://urban-backend.azurewebsites.net/api/rankings
curl https://urban-backend.azurewebsites.net/api/rankings/top?limit=10
curl https://urban-backend.azurewebsites.net/api/rankings/[city-name]
```

## Next Steps

1. ✓ Populate Supabase (this guide)
2. Set Vercel environment variables (see VERCEL_DEPLOYMENT.md)
3. Test frontend at https://urban-livability-analysis-sysytem.vercel.app
4. Monitor backend logs in Azure App Service
