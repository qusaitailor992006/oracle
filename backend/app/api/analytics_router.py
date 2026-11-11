from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.analytics_service import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Executive Analytics"])

@router.get("/dashboard")
def get_executive_dashboard(db: Session = Depends(get_db)):
    """Returns core enterprise financial performance, ARR, margins, and anomaly scorecards."""
    return analytics_service.get_executive_overview(db)
