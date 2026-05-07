# UrbanPulse IQ - Phase 1 Foundation

**India's Urban Livability Intelligence Platform**

## 📋 Phase 1: Foundation Overview

Phase 1 sets up the foundational architecture for UrbanPulse IQ, including:

- ✅ Frontend scaffolding with Next.js, TypeScript, TailwindCSS
- ✅ Dashboard UI with professional design system
- ✅ Backend API structure with FastAPI
- ✅ Database schema planning (PostgreSQL)
- ✅ Data pipeline architecture

### Timeline
**Week 1-2**: Dataset consolidation, schema planning, backend architecture, UI wireframes

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15
- Docker (optional)

### Option 1: Local Development Setup

#### 1. Clone and Setup Environment
```bash
cd /workspaces/Urban-Livability-Analysis-Sysytem

# Copy environment file
cp .env.example .env

# Update .env with your database credentials
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (when ready)
# alembic upgrade head

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Option 2: Docker Setup

```bash
# Build and run all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Database: `localhost:5432`

---

## 📁 Project Structure

```
Urban-Livability-Analysis-Sysytem/
├── frontend/                    # Next.js Application
│   ├── src/
│   │   ├── app/                # App routes & layouts
│   │   │   ├── page.tsx        # Dashboard (Overview)
│   │   │   ├── comparison/     # City Comparison
│   │   │   ├── analytics/      # EDA Analytics
│   │   │   ├── map/            # Interactive Maps
│   │   │   ├── reports/        # Reports & Insights
│   │   │   └── layout.tsx      # Root layout
│   │   └── components/         # React components
│   │       ├── layout/         # Layout components (Sidebar, Header)
│   │       ├── dashboard/      # Dashboard components
│   │       └── ui/             # Reusable UI components
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── Dockerfile
│
├── backend/                     # FastAPI Application
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── routes/                 # API routes
│   │   ├── rankings.py         # Rankings API
│   │   ├── cities.py           # Cities API
│   │   ├── analytics.py        # Analytics API
│   │   └── maps.py             # Maps API
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml          # Docker services
├── .env.example                # Environment variables template
├── .gitignore
├── DOCS.md                     # Complete product documentation
├── README.md                   # Original project README
└── Urban_Livability_EDA_Report.ipynb  # Research report
```

---

## 🎨 Design System

### Color Palette
- **Primary**: `#17324D` (Dark Blue)
- **Secondary**: `#4B647D` (Slate Blue)
- **Accent**: `#2F7E79` (Teal)
- **Surface**: `#F8FAFC` (Off White)
- **Border**: `#E8ECF1` (Light Gray)
- **Text**: `#2B2B2B` (Dark Gray)

### Typography
- **Headings**: Montserrat SemiBold
- **Body**: Inter
- **Metrics**: Inter SemiBold

---

## 📊 Dashboard Modules

### 1. Overview Dashboard (/)
Displays national-level urban livability intelligence:
- KPI cards (avg score, best city, pollution, safety, water risk)
- City ranking bar chart
- Urban stress indicators
- AI-generated insights panel

### 2. City Comparison (/comparison)
Multi-city comparative analysis:
- City selection (2-5 cities)
- Radar charts for category comparison
- Comparison tables
- Strength/weakness analysis

### 3. EDA Analytics (/analytics)
Research-backed analytics:
- **AQI Analytics**: PM2.5 levels, pollution severity
- **Crime Analytics**: Crime trends, women safety analysis
- **Water Intelligence**: Groundwater, contamination
- **Traffic Intelligence**: Congestion, bottlenecks

### 4. Map Intelligence (/map)
Geo-spatial visualization:
- Livability choropleth heatmap
- AQI heat layer
- Crime density markers
- Water stress overlays

### 5. Reports (/reports)
Export and generate reports:
- PDF exports
- CSV analytics
- Comparison reports
- Anomaly detection reports

---

## 🔌 API Endpoints

### Rankings API
- `GET /api/rankings` - Get all city rankings
- `GET /api/rankings/top` - Get top cities
- `GET /api/rankings/bottom` - Get bottom cities
- `GET /api/rankings/{city_id}` - Get specific city ranking

### Cities API
- `GET /api/cities` - Get all cities
- `GET /api/cities/{city_id}` - Get specific city
- `POST /api/cities` - Create new city

### Analytics API
- `GET /api/analytics/aqi` - AQI analytics
- `GET /api/analytics/crime` - Crime analytics
- `GET /api/analytics/water` - Water intelligence
- `GET /api/analytics/traffic` - Traffic analytics
- `GET /api/analytics/correlation` - Correlation matrix

### Maps API
- `GET /api/maps/livability` - Livability heatmap data
- `GET /api/maps/aqi-layer` - AQI heat layer
- `GET /api/maps/crime-density` - Crime density layer
- `GET /api/maps/water-stress` - Water stress layer

---

## 📈 Weighted Scoring Model

| Category   | Weight |
|-----------|--------|
| Crime     | 0.15   |
| Healthcare| 0.12   |
| Water     | 0.12   |
| Education | 0.10   |
| Sanitation| 0.10   |
| Pollution | 0.10   |
| Traffic   | 0.10   |
| Cost      | 0.10   |
| Population| 0.06   |
| Transport | 0.05   |

**Scoring Formula**: L = Σ(w_i × x_i)

---

## 🗄️ Database Schema

### Cities Table
```sql
- id (PK)
- city_name (Unique, Indexed)
- state
- latitude, longitude
- population
- tier (Tier-1/2/3)
- created_at, updated_at
```

### Livability Scores Table
```sql
- id (PK)
- city_id (FK)
- overall_score
- rank
- percentile
- timestamp
```

### Category Scores Table
```sql
- id (PK)
- city_id (FK)
- crime_score, healthcare_score, ... (10 categories)
- timestamp
```

### Raw Metrics Table
```sql
- id (PK)
- city_id (FK)
- aqi, pm25, pm10
- congestion_index, rent_affordability, crime_rate
- literacy_rate, healthcare_facilities
- timestamp
```

---

## 🔄 Data Pipeline

1. **Ingestion**: Data from NCRB, CPCB, TomTom, Census, etc.
2. **Cleaning**: Missing value imputation, unit standardization
3. **Normalization**: Min-Max scaling for positive/negative metrics
4. **Scoring**: Weighted aggregation
5. **Ranking**: Sort by livability score
6. **Visualization**: API → Dashboard Charts

---

## 🛠️ Development Workflow

### Adding a New Dashboard Page
1. Create page file in `frontend/src/app/[feature]/page.tsx`
2. Import layout components (Sidebar, Header)
3. Use TailwindCSS + Framer Motion for styling/animations
4. Fetch data from backend API using axios
5. Display with Recharts/ECharts visualizations

### Adding a New API Endpoint
1. Create route file in `backend/routes/`
2. Define route with FastAPI
3. Return Pydantic schema responses
4. Add to router in `main.py`
5. Test with `http://localhost:8000/docs`

---

## 📝 Available Commands

### Frontend
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

### Backend
```bash
uvicorn main:app --reload           # Start dev server
python -m pip install -r requirements.txt  # Install deps
```

### Docker
```bash
docker-compose up                   # Start all services
docker-compose down                 # Stop services
docker-compose logs -f backend      # View backend logs
```

---

## 🔐 Environment Variables

See `.env.example` for all required variables:
- `DATABASE_URL`: PostgreSQL connection string
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `ENVIRONMENT`: development/production
- `DEBUG`: Enable/disable debug mode

---

## 📚 Next Steps (Phase 2-3)

- [ ] Database migration setup (Alembic)
- [ ] Data cleaning pipeline implementation
- [ ] Normalization engine development
- [ ] Scoring engine automation
- [ ] Interactive map implementation (Mapbox)
- [ ] User authentication
- [ ] Advanced EDA visualizations
- [ ] Report generation engine

---

## 📞 Support

For issues or questions:
1. Check the DOCS.md for complete product specification
2. Review Urban_Livability_EDA_Report.ipynb for research background
3. Check API documentation at `http://localhost:8000/docs`

---

**UrbanPulse IQ** © 2026 | India's Urban Intelligence Platform
