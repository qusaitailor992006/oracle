from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models.oracle_models import InvestigationCase
from backend.app.schemas.oracle_schemas import InvestigationCaseBase, InvestigationActionRequest

router = APIRouter(prefix="/api/investigations", tags=["AI Investigation Engine"])

@router.get("", response_model=List[InvestigationCaseBase])
def get_all_investigations(db: Session = Depends(get_db)):
    return db.query(InvestigationCase).order_by(InvestigationCase.created_at.desc()).all()

@router.get("/{case_id}", response_model=InvestigationCaseBase)
def get_investigation_detail(case_id: str, db: Session = Depends(get_db)):
    case = db.query(InvestigationCase).filter(InvestigationCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Investigation case not found")
    return case

@router.post("/{case_id}/action")
def review_recommendation(case_id: str, action: InvestigationActionRequest, db: Session = Depends(get_db)):
    case = db.query(InvestigationCase).filter(InvestigationCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Investigation case not found")
        
    case.human_approved = action.approved
    case.status = "RESOLVED" if action.approved else "REJECTED"
    db.commit()
    db.refresh(case)
    return {
        "status": "success",
        "case_id": case.id,
        "new_status": case.status,
        "human_approved": case.human_approved
    }
