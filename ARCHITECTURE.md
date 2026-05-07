# UrbanPulse IQ - Project Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │        Next.js Frontend (TypeScript + React)            │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  Sidebar Navigation    │    Header (Search)     │   │   │
│  │  ├──────────────────────────────────────────────────┤   │   │
│  │  │                   Main Content                   │   │   │
│  │  │  • Dashboard Overview                            │   │   │
│  │  │  • City Comparison                               │   │   │
│  │  │  • EDA Analytics                                 │   │   │
│  │  │  • Map Intelligence                              │   │   │
│  │  │  • Reports & Insights                            │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  Design System:                                       │   │
│  │  • TailwindCSS (Styling)                             │   │
│  │  • Framer Motion (Animations)                        │   │
│  │  • Recharts/ECharts (Visualizations)                │   │
│  │  • Zustand (State Management)                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                              ↓                               │
│                     HTTP/REST API Calls                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       API GATEWAY LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│         FastAPI (Python) - Port 8000                           │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  CORS Middleware  │  Request Validation             │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ROUTE/SERVICE LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │  Rankings    │ │  Cities      │ │  Analytics   │            │
│  │  Endpoints   │ │  Endpoints   │ │  Endpoints   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐ ┌──────────────┐                             │
│  │  Maps        │ │  Comparison  │                             │
│  │  Endpoints   │ │  Endpoints   │                             │
│  └──────────────┘ └──────────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   ANALYTICS ENGINE LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │  Scoring Engine                                     │       │
│  │  • Normalization (Min-Max Scaling)                 │       │
│  │  • Weighted Aggregation (10 categories)            │       │
│  │  • Percentile Ranking                              │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │  Data Processing                                    │       │
│  │  • Pandas (Data Manipulation)                       │       │
│  │  • NumPy (Numerical Computation)                    │       │
│  │  • Scikit-learn (Anomaly Detection)                 │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│         PostgreSQL (Port 5432)                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │                                                      │      │
│  │  Tables:                                            │      │
│  │  • cities (city_name, state, lat, lng, tier)       │      │
│  │  • livability_scores (overall_score, rank)         │      │
│  │  • category_scores (10 category metrics)           │      │
│  │  • raw_metrics (AQI, PM2.5, crime, rent, etc)      │      │
│  │                                                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Hierarchy

### Frontend Components

```
App Layout
├── Sidebar
│   ├── Logo
│   ├── Navigation Menu
│   └── Settings
├── Header
│   ├── Search Bar
│   ├── Notifications
│   └── User Profile
└── Main Content
    ├── Dashboard (/)
    │   ├── KPI Cards (5 metrics)
    │   ├── CityRankingChart
    │   ├── UrbanStressIndicators
    │   └── InsightsPanel
    ├── Comparison (/comparison)
    │   ├── City Selector
    │   ├── Radar Charts
    │   └── Comparison Table
    ├── Analytics (/analytics)
    │   ├── AQI Tab
    │   ├── Crime Tab
    │   ├── Water Tab
    │   └── Traffic Tab
    ├── Map (/map)
    │   ├── Mapbox Container
    │   └── Layer Controls
    └── Reports (/reports)
        ├── Report Generator
        └── Report List
```

---

## Data Flow

### Ranking Generation Flow
```
Raw Data (CSV/APIs)
    ↓
[Backend] Clean & Validate
    ↓
[Analytics] Normalize Metrics
    ↓
[Analytics] Apply Weights (10 categories)
    ↓
[Database] Store Scores & Rankings
    ↓
[API] Return Ranked Cities
    ↓
[Frontend] Display Rankings & Charts
```

### City Comparison Flow
```
User Selects Cities (2-5)
    ↓
[Frontend] Send City IDs to API
    ↓
[Backend] Query Category Scores
    ↓
[API] Return Comparison Data
    ↓
[Frontend] Render Radar Charts & Tables
```

---

## Database Schema Relationships

```
┌─────────────────────┐
│      cities         │
├─────────────────────┤
│ id (PK)             │
│ city_name           │
│ state               │
│ latitude            │
│ longitude           │
│ population          │
│ tier                │
│ created_at          │
└──────────┬──────────┘
           │ (1:N)
           │
    ┌──────┴──────────────────┬─────────────────┐
    │                         │                 │
    ↓                         ↓                 ↓
┌──────────────────┐ ┌─────────────────┐ ┌──────────────┐
│livability_scores │ │category_scores  │ │ raw_metrics  │
├──────────────────┤ ├─────────────────┤ ├──────────────┤
│id (PK)           │ │id (PK)          │ │id (PK)       │
│city_id (FK)      │ │city_id (FK)     │ │city_id (FK)  │
│overall_score     │ │crime_score      │ │aqi           │
│rank              │ │healthcare_score │ │pm25          │
│percentile        │ │water_score      │ │congestion    │
│timestamp         │ │... (10 total)   │ │... etc       │
│                  │ │timestamp        │ │timestamp     │
└──────────────────┘ └─────────────────┘ └──────────────┘
```

---

## API Routes Structure

```
/api
├── /rankings
│   ├── GET / (all rankings)
│   ├── GET /top (top 5 cities)
│   ├── GET /bottom (bottom 5 cities)
│   └── GET /{city_id} (specific city)
│
├── /cities
│   ├── GET / (all cities)
│   ├── GET /{city_id} (specific city)
│   └── POST / (create city)
│
├── /analytics
│   ├── GET /aqi (AQI analytics)
│   ├── GET /crime (crime data)
│   ├── GET /water (water metrics)
│   ├── GET /traffic (traffic metrics)
│   └── GET /correlation (correlation matrix)
│
└── /maps
    ├── GET /livability (heatmap data)
    ├── GET /aqi-layer (AQI layer)
    ├── GET /crime-density (crime markers)
    └── GET /water-stress (water risk)
```

---

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14 | React framework |
| Frontend | TypeScript | Type safety |
| Frontend | TailwindCSS | Styling |
| Frontend | Framer Motion | Animations |
| Frontend | Recharts | Charts |
| Frontend | Zustand | State management |
| Backend | FastAPI | REST API |
| Backend | Python 3.11 | Backend language |
| Backend | SQLAlchemy | ORM |
| Backend | Pandas | Data processing |
| Database | PostgreSQL 15 | Relational DB |
| Container | Docker | Containerization |
| Deployment | Vercel (Frontend) | Hosting |
| Deployment | Railway/Render | Backend hosting |

---

## Current Status (Phase 1)

### ✅ Completed
- [ x ] Project structure initialization
- [ x ] Frontend scaffolding (Next.js + TypeScript)
- [ x ] Dashboard UI components (professional design)
- [ x ] Page layouts (Overview, Comparison, Analytics, Map, Reports)
- [ x ] Backend API structure (FastAPI)
- [ x ] Database schema planning
- [ x ] API endpoints with mock data
- [ x ] Docker setup (compose file, Dockerfiles)
- [ x ] Documentation (PHASE1_SETUP.md)

### 🔄 Phase 2 Tasks
- [ ] Database migrations (Alembic)
- [ ] Real data integration
- [ ] Scoring engine automation
- [ ] Data pipeline implementation
- [ ] Advanced visualizations (Mapbox)

---

## Notes

- All API responses use Pydantic schemas for validation
- Frontend components use Framer Motion for smooth animations
- Design follows professional analytics dashboard patterns
- Database schema designed for scalability (100+ cities)
- CORS configured for local development

---

**Last Updated**: May 7, 2026
