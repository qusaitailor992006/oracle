import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.models.oracle_models import *
from backend.app.services.synthetic_data_engine import synthetic_business_engine
from backend.app.api.query_router import router as query_router
from backend.app.api.analytics_router import router as analytics_router
from backend.app.api.investigations_router import router as investigations_router
from backend.app.api.reports_router import router as reports_router

# Initialize Database Schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Autonomous Enterprise Decision Intelligence Engine simulating senior business analyst workflows.",
    version="1.0.0"
)

# Enable CORS for local Vite and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(query_router)
app.include_router(analytics_router)
app.include_router(investigations_router)
app.include_router(reports_router)

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        # Automatically seed synthetic business dataset on initial launch
        synthetic_business_engine.seed_initial_enterprise_data(db)
    finally:
        db.close()

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "platform": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.PORT, reload=True)
