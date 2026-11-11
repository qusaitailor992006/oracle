import os
import re
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/oracle.db")

connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

if "sqlite" in DATABASE_URL:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Strict Read-Only SQL Sanitizer & Validator
FORBIDDEN_SQL_KEYWORDS = [
    r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b", r"\bDROP\b",
    r"\bALTER\b", r"\bCREATE\b", r"\bTRUNCATE\b", r"\bATTACH\b",
    r"\bDETACH\b", r"\bPRAGMA\b", r"\bREPLACE\b", r"\bGRANT\b",
    r"\bREVOKE\b", r"\bEXEC\b", r"\bEXECUTE\b"
]

def execute_readonly_query(sql_query: str, max_rows: int = 200):
    """
    Validates and executes strictly read-only SQL queries against the analytical database.
    Prevents DDL/DML injection attacks.
    """
    clean_query = sql_query.strip().rstrip(";")
    
    # 1. Regex check for dangerous mutation keywords
    for pattern in FORBIDDEN_SQL_KEYWORDS:
        if re.search(pattern, clean_query, re.IGNORECASE):
            raise ValueError(f"Security Violation: Query contains prohibited write/DDL operation matching '{pattern}'")
            
    # 2. Must start with SELECT or WITH
    if not re.match(r"^(SELECT|WITH)\b", clean_query, re.IGNORECASE):
        raise ValueError("Security Violation: Only SELECT or WITH queries are permitted.")
        
    with engine.connect() as conn:
        result = conn.execute(text(clean_query))
        columns = list(result.keys())
        rows = [dict(zip(columns, row)) for row in result.fetchmany(max_rows)]
        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "executed_sql": clean_query
        }
