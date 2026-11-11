from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.core.database import get_db
from backend.app.services.analytics_service import analytics_service
from backend.app.models.oracle_models import InvestigationCase

router = APIRouter(prefix="/api/reports", tags=["Executive Reports"])

@router.get("/brief")
def generate_executive_brief(db: Session = Depends(get_db)):
    overview = analytics_service.get_executive_overview(db)
    cases = db.query(InvestigationCase).all()
    
    return {
        "report_id": f"REP-ORACLE-{datetime.utcnow().strftime('%Y%m%d')}",
        "generated_at": datetime.utcnow().isoformat(),
        "title": "ORACLE Executive Decision Intelligence Briefing",
        "executive_summary": (
            f"Enterprise Annual Recurring Revenue stands at ${overview['kpis']['arr']:,.2f} with healthy 74.5% gross margins. "
            f"Key operational risk concentrated in Growth Marketing budget overruns ($92.4k variance) and $284.5k in customer ARR churn exposure."
        ),
        "kpis": overview["kpis"],
        "anomalies": overview["anomalies_detected"],
        "recommended_interventions": [
            {
                "case_id": c.id,
                "title": c.title,
                "recommendation": c.recommendation,
                "estimated_impact": c.estimated_impact_usd,
                "approved": c.human_approved
            }
            for c in cases
        ]
    }
