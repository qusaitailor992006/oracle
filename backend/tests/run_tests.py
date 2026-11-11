import sys
import unittest
from backend.app.core.database import execute_readonly_query, SessionLocal
from backend.app.services.nl_query_engine import nl_query_engine
from backend.app.services.synthetic_data_engine import synthetic_business_engine
from backend.app.services.analytics_service import analytics_service

class TestOracleCore(unittest.TestCase):
    def setUp(self):
        from backend.app.core.database import Base, engine
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            synthetic_business_engine.seed_initial_enterprise_data(db)
        finally:
            db.close()

    def test_sql_injection_defense(self):
        """Verify that malicious DDL/DML statements are blocked by read-only validator."""
        malicious = [
            "DROP TABLE customers;",
            "DELETE FROM orders WHERE id = 'ORD-1';",
            "UPDATE financial_records SET revenue = 9999999;",
            "INSERT INTO departments (name) VALUES ('Hacked');",
            "ALTER TABLE employees ADD COLUMN hacked TEXT;"
        ]
        for q in malicious:
            with self.assertRaises(ValueError):
                execute_readonly_query(q)

    def test_valid_select_query(self):
        """Verify that safe SELECT queries execute and return structured rows."""
        res = execute_readonly_query("SELECT 1 as test_col, 'ORACLE' as platform_name;")
        self.assertEqual(res["row_count"], 1)
        self.assertEqual(res["columns"], ["test_col", "platform_name"])
        self.assertEqual(res["rows"][0]["platform_name"], "ORACLE")

    def test_nl_query_engine_processing(self):
        """Verify that natural language query parser returns actionable data and insights."""
        res = nl_query_engine.process_query("What are our top most profitable products?")
        self.assertTrue(res["success"])
        self.assertIn("SELECT", res["generated_sql"].upper())
        self.assertGreater(res["row_count"], 0)
        self.assertGreater(len(res["key_insights"]), 0)

    def test_executive_kpi_calculations(self):
        """Verify that financial aggregations compute valid non-zero figures."""
        db = SessionLocal()
        try:
            overview = analytics_service.get_executive_overview(db)
            kpis = overview["kpis"]
            self.assertGreater(kpis["arr"], 0)
            self.assertGreater(kpis["gross_margin_pct"], 50.0)
            self.assertGreater(len(overview["financial_trend"]), 0)
            self.assertGreater(len(overview["department_breakdown"]), 0)
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()
