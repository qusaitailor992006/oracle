from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str
    user_email: Optional[str] = "executive@oracle.internal"

class QueryResponse(BaseModel):
    success: bool
    user_query: str
    generated_sql: Optional[str] = None
    query_source: Optional[str] = None
    row_count: int = 0
    columns: List[str] = []
    data: List[Dict[str, Any]] = []
    executive_summary: Optional[str] = None
    key_insights: List[str] = []
    recommended_action: Optional[str] = None
    confidence_score: float = 0.0
    error: Optional[str] = None

class InvestigationCaseBase(BaseModel):
    id: str
    title: str
    user_query: str
    status: str
    department: Optional[str]
    hypothesis: Optional[str]
    findings: List[str] = []
    generated_sql: Optional[str]
    evidence_data: Optional[Dict[str, Any]] = {}
    recommendation: Optional[str]
    estimated_impact_usd: float = 0.0
    confidence_score: float = 0.0
    human_approved: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class InvestigationActionRequest(BaseModel):
    approved: bool
    notes: Optional[str] = "Decision rendered by executive."
