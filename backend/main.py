from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="UrbanPulse IQ API",
    description="India's Urban Livability Intelligence Platform",
    version="0.1.0"
)

# CORS Configuration
default_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "https://urban-livability-analysis-sysytem.vercel.app",
]
env_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()]
origins = list(dict.fromkeys(default_origins + env_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "UrbanPulse IQ API",
        "version": "0.1.0"
    }

# Root Endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to UrbanPulse IQ API",
        "version": "0.1.0",
        "docs": "/docs"
    }

# Import route modules
try:
    from routes import rankings, cities, analytics, maps, reports
    
    app.include_router(rankings.router, prefix="/api/rankings", tags=["rankings"])
    app.include_router(cities.router, prefix="/api/cities", tags=["cities"])
    app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
    app.include_router(maps.router, prefix="/api/maps", tags=["maps"])
    app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
except ImportError as e:
    print(f"Note: Some routes not yet implemented: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
