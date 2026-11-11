import pytest
from backend.app.core.database import execute_readonly_query, SessionLocal
from backend.app.services.nl_query_engine import nl_query_engine
from backend.app.services.analytics_service import analytics_service

def test_readonly_sql_protection():
    """Verify that malicious DDL/DML statements are strictly blocked."""
    malicious_queries = [
        "DROP TABLE customers;",
        "DELETE FROM orders WHERE id = 'ORD-1';",
        "UPDATE financial_records SET revenue = 9999999;",
        "INSERT INTO departments (name) VALUES ('Hacked');",
        "ALTER TABLE employees ADD COLUMN hacked TEXT;"
    ]
    for q in malicious_queries:
        with pytest.raises(ValueError) as excinfo:
            execute_readonly_query(q)
        assert "Security Violation" in str(excinfo.value)

def test_valid_select_query():
    """Verify that safe SELECT queries execute and return structured rows."""
    res = execute_readonly_query("SELECT 1 as test_col, 'ORACLE' as platform_name;")
    assert res["row_count"] == 1
    assert res["columns"] == ["test_col", "platform_name"]
    assert res["rows"][0]["platform_name"] == "ORACLE"

def test_nl_query_engine_fallback():
    """Verify that natural language query parser returns actionable data and insights."""
    res = nl_query_engine.process_query("What are our top most profitable products?")
    assert res["success"] is True
    assert "generated_sql" in res
    assert "SELECT" in res["generated_sql"].upper()
    assert res["row_count"] > 0
    assert len(res["key_insights"]) > 0

def test_executive_kpi_calculations():
    """Verify that financial aggregations compute valid non-zero figures."""
    db = SessionLocal()
    try:
        overview = analytics_service.get_executive_overview(db)
        kpis = overview["kpis"]
        assert kpis["arr"] > 0
        assert kpis["gross_margin_pct"] > 50.0
        assert len(overview["financial_trend"]) > 0
        assert len(overview["department_breakdown"]) > 0
    finally:
        db.close()
