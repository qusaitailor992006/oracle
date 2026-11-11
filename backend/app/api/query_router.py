import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.oracle_schemas import QueryRequest, QueryResponse
from backend.app.services.nl_query_engine import nl_query_engine
from backend.app.models.oracle_models import QueryAuditLog

router = APIRouter(prefix="/api/query", tags=["AI Business Query Engine"])

@router.post("", response_model=QueryResponse)
def execute_business_query(payload: QueryRequest, db: Session = Depends(get_db)):
    """
    Translates executive natural language query to validated read-only SQL,
    executes it against enterprise data, and returns evidence-backed business insights.
    """
    start_time = time.time()
    result = nl_query_engine.process_query(payload.query)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    # Audit logging for compliance
    if result.get("generated_sql"):
        audit = QueryAuditLog(
            user_email=payload.user_email or "executive@oracle.internal",
            natural_language_query=payload.query,
            executed_sql=result["generated_sql"],
            execution_time_ms=duration_ms,
            row_count=result.get("row_count", 0)
        )
        db.add(audit)
        db.commit()

    return result
