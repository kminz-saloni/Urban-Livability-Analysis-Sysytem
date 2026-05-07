# ⚠️ Supabase Database - Quick Start (3 Easy Steps)

## Current Status
✅ Backend deployed on Azure  
✅ Frontend deployed on Vercel  
❌ **Supabase database is empty** ← You are here

## Step 1: Create Tables in Supabase

1. Go to: https://app.supabase.com
2. Select your project: **Urban Livability Analysis**
3. Go to **SQL Editor** (left sidebar)
4. Click **New Query**
5. Paste this SQL and run it:

```sql
-- Create all required tables
CREATE TABLE IF NOT EXISTS public.cities (
  id BIGSERIAL PRIMARY KEY,
  city_name VARCHAR(100) UNIQUE NOT NULL,
  state VARCHAR(50),
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  population INTEGER,
  tier VARCHAR(20),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.raw_metrics (
  id BIGSERIAL PRIMARY KEY,
  city_id BIGINT REFERENCES public.cities(id),
  aqi DOUBLE PRECISION,
  pm25 DOUBLE PRECISION,
  pm10 DOUBLE PRECISION,
  congestion_index DOUBLE PRECISION,
  rent_affordability DOUBLE PRECISION,
  crime_rate DOUBLE PRECISION,
  literacy_rate DOUBLE PRECISION,
  timestamp DATE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.category_scores (
  id BIGSERIAL PRIMARY KEY,
  city_id BIGINT REFERENCES public.cities(id),
  crime_score DOUBLE PRECISION,
  healthcare_score DOUBLE PRECISION,
  water_score DOUBLE PRECISION,
  education_score DOUBLE PRECISION,
  sanitation_score DOUBLE PRECISION,
  pollution_score DOUBLE PRECISION,
  traffic_score DOUBLE PRECISION,
  cost_score DOUBLE PRECISION,
  population_score DOUBLE PRECISION,
  transport_score DOUBLE PRECISION,
  timestamp DATE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.livability_scores (
  id BIGSERIAL PRIMARY KEY,
  city_id BIGINT REFERENCES public.cities(id),
  overall_score DOUBLE PRECISION,
  rank INTEGER,
  percentile DOUBLE PRECISION,
  timestamp DATE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_cities_name ON public.cities(city_name);
CREATE INDEX IF NOT EXISTS idx_raw_metrics_city ON public.raw_metrics(city_id);
CREATE INDEX IF NOT EXISTS idx_category_scores_city ON public.category_scores(city_id);
CREATE INDEX IF NOT EXISTS idx_livability_scores_city ON public.livability_scores(city_id);
```

✅ **Expected Result:** "Query executed successfully"

---

## Step 2: Populate with Sample Data

Still in **SQL Editor**, run this:

```sql
-- Insert sample cities
INSERT INTO public.cities (city_name, state, latitude, longitude, population, tier) VALUES
('Kozhikode', 'Kerala', 11.2588, 75.7804, 600000, 'Tier-2'),
('Coimbatore', 'Tamil Nadu', 11.0060, 76.9855, 2100000, 'Tier-2'),
('Bangalore', 'Karnataka', 12.9716, 77.5946, 8436675, 'Tier-1'),
('Hyderabad', 'Telangana', 17.3850, 78.4867, 6809970, 'Tier-1'),
('Pune', 'Maharashtra', 18.5204, 73.8567, 3124458, 'Tier-1'),
('Chennai', 'Tamil Nadu', 13.0827, 80.2707, 4646732, 'Tier-1'),
('Kolkata', 'West Bengal', 22.5726, 88.3639, 14681900, 'Tier-1'),
('Delhi', 'Delhi', 28.7041, 77.1025, 16787941, 'Tier-1'),
('Mumbai', 'Maharashtra', 19.0760, 72.8777, 20411000, 'Tier-1'),
('Ahmedabad', 'Gujarat', 23.0225, 72.5714, 7214225, 'Tier-1');

-- Insert raw metrics for each city (10 cities = 10 metrics)
INSERT INTO public.raw_metrics (city_id, aqi, pm25, pm10, congestion_index, rent_affordability, crime_rate, literacy_rate) VALUES
(1, 85, 45, 75, 35, 45, 4.2, 95.5),
(2, 92, 48, 82, 42, 48, 4.8, 94.0),
(3, 88, 50, 80, 65, 52, 5.2, 92.0),
(4, 90, 52, 85, 55, 55, 4.5, 96.0),
(5, 85, 48, 78, 50, 50, 4.0, 95.0),
(6, 95, 55, 95, 70, 60, 5.5, 93.0),
(7, 110, 65, 120, 75, 40, 6.2, 91.0),
(8, 120, 70, 130, 80, 38, 6.8, 90.0),
(9, 130, 75, 145, 85, 35, 7.0, 89.0),
(10, 100, 58, 105, 72, 58, 5.8, 94.5);

-- Insert category scores (normalized 0-100)
INSERT INTO public.category_scores (city_id, crime_score, healthcare_score, water_score, education_score, sanitation_score, pollution_score, traffic_score, cost_score, population_score, transport_score) VALUES
(1, 75, 82, 78, 88, 85, 72, 70, 45, 75, 82),
(2, 70, 80, 75, 85, 80, 68, 68, 48, 75, 80),
(3, 68, 88, 72, 90, 82, 70, 60, 52, 80, 85),
(4, 72, 85, 70, 88, 78, 65, 65, 50, 78, 83),
(5, 78, 90, 82, 92, 88, 73, 72, 55, 82, 88),
(6, 65, 78, 68, 80, 72, 60, 55, 45, 70, 75),
(7, 60, 75, 65, 78, 70, 55, 50, 52, 85, 70),
(8, 55, 70, 60, 75, 65, 50, 45, 55, 85, 65),
(9, 50, 65, 58, 72, 60, 45, 40, 60, 90, 60),
(10, 62, 82, 72, 88, 78, 58, 58, 48, 75, 80);

-- Insert livability scores and rankings
INSERT INTO public.livability_scores (city_id, overall_score, rank, percentile) VALUES
(5, 79.7, 1, 90),
(1, 77.1, 2, 80),
(3, 75.9, 3, 70),
(4, 73.6, 4, 60),
(2, 72.4, 5, 50),
(10, 71.8, 6, 40),
(6, 68.9, 7, 30),
(5, 65.2, 8, 20),
(7, 62.3, 9, 10),
(8, 58.1, 10, 5);
```

✅ **Expected Result:** "Query executed successfully" for each INSERT

---

## Step 3: Verify Data

Run this query to verify:

```sql
SELECT c.city_name, ls.overall_score, ls.rank, c.state
FROM public.cities c
JOIN public.livability_scores ls ON c.id = ls.city_id
ORDER BY ls.rank
LIMIT 10;
```

✅ **Expected:** 10 cities with ranks and scores

---

## Step 4: Test the Full Stack

### Check Backend API:
```bash
curl https://urban-backend.azurewebsites.net/api/rankings | head -20
```

### Check Frontend:
Visit: https://urban-livability-analysis-sysytem.vercel.app

You should see:
- ✅ City rankings
- ✅ Livability scores
- ✅ Map with locations
- ✅ Analytics data

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Permission denied" in Supabase | Use authenticated dashboard (you should be logged in) |
| "Relation already exists" | Run `DROP TABLE public.livability_scores CASCADE;` first |
| Data not showing in frontend | Set env vars in Vercel (see VERCEL_DEPLOYMENT.md) |
| Backend returns empty | Verify DATABASE_URL in Azure App Service settings |

---

## Next Steps After Population

1. ✅ Tables created
2. ✅ Data populated  
3. 👉 **Set Vercel environment variables** (see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md))
4. Test frontend access
5. Monitor logs

---

## Resources

- **Supabase Dashboard:** https://app.supabase.com
- **Azure Backend:** https://urban-backend.azurewebsites.net
- **Frontend:** https://urban-livability-analysis-sysytem.vercel.app
- **Docs:** See [SUPABASE_SETUP_GUIDE.md](SUPABASE_SETUP_GUIDE.md) for advanced options
