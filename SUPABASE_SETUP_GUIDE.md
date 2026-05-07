# How to Populate Supabase Database

Since the dev container cannot reach Supabase directly, here are the recommended approaches:

## Option 1: Use Supabase Dashboard (Easiest - Recommended)

1. **Go to Supabase Dashboard:**
   - URL: https://app.supabase.com
   - Project: Urban Livability Analysis

2. **Create Tables via SQL Editor:**
   
   ```sql
   -- Create cities table
   CREATE TABLE IF NOT EXISTS cities (
     id SERIAL PRIMARY KEY,
     city_name VARCHAR(100) UNIQUE NOT NULL,
     state VARCHAR(50),
     latitude FLOAT,
     longitude FLOAT,
     population INTEGER,
     tier VARCHAR(20),
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
   );

   -- Create raw_metrics table
   CREATE TABLE IF NOT EXISTS raw_metrics (
     id SERIAL PRIMARY KEY,
     city_id INTEGER,
     aqi FLOAT,
     pm25 FLOAT,
     pm10 FLOAT,
     congestion_index FLOAT,
     rent_affordability FLOAT,
     crime_rate FLOAT,
     literacy_rate FLOAT,
     healthcare_facilities INTEGER,
     timestamp DATE DEFAULT NOW()
   );

   -- Create category_scores table
   CREATE TABLE IF NOT EXISTS category_scores (
     id SERIAL PRIMARY KEY,
     city_id INTEGER,
     crime_score FLOAT,
     healthcare_score FLOAT,
     water_score FLOAT,
     education_score FLOAT,
     sanitation_score FLOAT,
     pollution_score FLOAT,
     traffic_score FLOAT,
     cost_score FLOAT,
     population_score FLOAT,
     transport_score FLOAT,
     timestamp DATE DEFAULT NOW()
   );

   -- Create livability_scores table
   CREATE TABLE IF NOT EXISTS livability_scores (
     id SERIAL PRIMARY KEY,
     city_id INTEGER,
     overall_score FLOAT,
     rank INTEGER,
     percentile FLOAT,
     timestamp DATE DEFAULT NOW(),
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

3. **Populate with Sample Data:**
   
   ```sql
   -- Insert a few sample cities
   INSERT INTO cities (city_name, state, latitude, longitude, population, tier)
   VALUES 
     ('Kozhikode', 'Kerala', 11.2588, 75.7804, 600000, 'Tier-2'),
     ('Coimbatore', 'Tamil Nadu', 11.0060, 76.9855, 2100000, 'Tier-2'),
     ('Bangalore', 'Karnataka', 12.9716, 77.5946, 8436675, 'Tier-1'),
     ('Hyderabad', 'Telangana', 17.3850, 78.4867, 6809970, 'Tier-1'),
     ('Pune', 'Maharashtra', 18.5204, 73.8567, 3124458, 'Tier-1');

   -- Insert raw metrics (after getting actual city IDs)
   INSERT INTO raw_metrics (city_id, aqi, pm25, pm10, congestion_index, crime_rate, literacy_rate)
   VALUES 
     (1, 85, 45, 75, 35, 4.2, 95.5),
     (2, 92, 48, 82, 42, 4.8, 94.0),
     (3, 88, 50, 80, 65, 5.2, 92.0),
     (4, 90, 52, 85, 55, 4.5, 96.0),
     (5, 85, 48, 78, 50, 4.0, 95.0);

   -- Insert category scores
   INSERT INTO category_scores (city_id, crime_score, healthcare_score, water_score, education_score, sanitation_score, pollution_score, traffic_score, cost_score, population_score, transport_score)
   VALUES 
     (1, 75, 82, 78, 88, 85, 72, 70, 45, 75, 82),
     (2, 70, 80, 75, 85, 80, 68, 68, 48, 75, 80),
     (3, 68, 88, 72, 90, 82, 70, 60, 52, 80, 85),
     (4, 72, 85, 70, 88, 78, 65, 65, 50, 78, 83),
     (5, 78, 90, 82, 92, 88, 73, 72, 55, 82, 88);

   -- Insert livability scores
   INSERT INTO livability_scores (city_id, overall_score, rank, percentile)
   VALUES 
     (1, 75, 3, 40),
     (2, 72, 4, 20),
     (3, 78, 1, 80),
     (4, 76, 2, 60),
     (5, 79, 1, 80);
   ```

4. **Verify Data:**
   ```sql
   SELECT c.city_name, ls.overall_score, ls.rank 
   FROM cities c
   JOIN livability_scores ls ON c.id = ls.city_id
   ORDER BY ls.rank;
   ```

## Option 2: Populate via Backend API (After Azure Deployment)

Once the backend is running on Azure, use the admin endpoints:

```bash
# Import the population script as a FastAPI endpoint
curl -X POST https://urban-backend.azurewebsites.net/admin/populate
```

(You would need to add this endpoint to the backend)

## Option 3: Use Migration Scripts with Flyway/Alembic

Create database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Create initial schema and seed data"

# Run migration
alembic upgrade head
```

## Option 4: Use Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link to project
supabase link --project-ref onwsdqfcisezshmvsmek

# Run SQL migration
supabase db push

# Seed data
supabase db seed
```

## Recommended Next Steps

1. **👉 Use Supabase Dashboard SQL Editor** (Option 1 - Easiest)
   - Copy the SQL from above
   - Paste into Supabase Dashboard SQL Editor
   - Execute

2. **Verify Backend Connection:**
   ```bash
   curl https://urban-backend.azurewebsites.net/api/rankings
   ```

3. **Check Frontend:**
   - Visit https://urban-livability-analysis-sysytem.vercel.app
   - Data should load from the backend

## Issues & Solutions

**Q: How do I find city IDs?**
```sql
SELECT id, city_name FROM cities;
```

**Q: How do I insert more cities?**
- Use the Supabase dashboard table editor
- Or run INSERT statements in SQL Editor

**Q: How do I bulk import data?**
- Use Supabase's import feature (CSV upload)
- Or use a Python script with REST API

**Q: Tables already exist?**
```sql
-- Check existing tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- If needed, drop and recreate
DROP TABLE IF EXISTS livability_scores CASCADE;
DROP TABLE IF EXISTS category_scores CASCADE;
DROP TABLE IF EXISTS raw_metrics CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
```
