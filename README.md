# ORACLE: Autonomous Enterprise Decision Intelligence Engine

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![SQLite WAL](https://img.shields.io/badge/SQLite-WAL%20Mode-003B57.svg)](https://www.sqlite.org/)
[![Groq LPU](https://img.shields.io/badge/Groq%20LPU-LLaMA%203.3%2070B-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ORACLE functions as an autonomous senior enterprise business analyst: translating natural language questions into safe read-only SQL, running multi-step investigations, and delivering evidence-backed recommendations with projected financial impacts.

---

## Key Capabilities

- **AI Natural Language Business Query Engine (NL-to-SQL)**: Interprets executive queries, converts them to validated read-only SQL, executes them against relational tables, and returns plain-English executive explanations.
- **SQL Security Sandbox**: AST and regex-level validation strictly restricting execution to `SELECT` statements (blocking `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `ATTACH`).
- **Financial & Business Intelligence**: Monitors Annual Recurring Revenue (ARR), Gross/Net Margins, operating cash flow, and 12-month trailing P&L curves.
- **Department Variance & Overrun Detection**: Tracks departmental budget allocations against actual expenditures, isolating cost overruns.
- **Customer Churn & Segment Analytics**: Evaluates customer segmentation (Enterprise, Mid-Market, SMB), cohort churn velocity, and exposed ARR.
- **Multi-Step Investigation Engine**: Formulates hypotheses, collects supporting telemetry, and projects financial impacts ($ USD).
- **Human-in-the-Loop Governance**: Requires explicit executive authorization before logging decisions.
- **Executive Dossier Export**: Formats exportable briefings for C-suite leadership.

---

## Architecture Flow

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             ORACLE ARCHITECTURE FLOW                             │
│                                                                                  │
│   [Executive User Inquiries]                                                     │
│               │                                                                  │
│               ▼                                                                  │
│   [Natural Language Query Engine] ───> [SQL Security Sandbox]                    │
│   - Groq LLaMA 3.3 / Semantic Parser    - AST & Keyword Mutation Validator       │
│                                         - Rejects DDL / DML                      │
│                                                       │                          │
│                                                       ▼                          │
│   [FastAPI Core Engine] ───────────────> [Relational Warehouse]                  │
│   - /api/query                           - SQLite WAL / PostgreSQL               │
│   - /api/analytics                       - Financials, Customers, Orders         │
│   - /api/investigations                  - Departments, Products                 │
│   - /api/reports                                      │                          │
│               │                                       ▼                          │
│               ├─────────────────────────> [Investigation Engine]                  │
│               │                            - Multi-Step Hypothesis Testing       │
│               │                            - Projected Financial Impact ($)      │
│               │                            - Human Authorization Gate            │
│               ▼                                                                  │
│   [Executive UI Presentation]                                                    │
│   - React 18 + Tailwind Interface                                                │
│   - Netlify-Ready Live Dashboard                                                 │
│   - Tabular Results & P&L Visualizer                                             │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start (Local Setup in 2 Minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Backend Setup & Run
```bash
git clone https://github.com/qusaitailor992006/oracle.git
cd oracle/backend

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate

pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
*API documentation automatically available at `http://127.0.0.1:8000/docs`.*

### 2. Standalone Live Dashboard
Simply open `live-app/index.html` in your browser, or deploy `live-app/` to **[Netlify Drop](https://app.netlify.com/drop)** for an instant public web application.

---

## Repository Structure

```
oracle/
├── backend/
│   ├── app/
│   │   ├── api/            # Query, Analytics, Investigations, Reports
│   │   ├── core/           # Config, SQLite WAL database, read-only SQL validator
│   │   ├── models/         # SQLAlchemy Relational Models (Departments, Customers, etc.)
│   │   ├── schemas/        # Pydantic validation schemas
│   │   └── services/       # NL-to-SQL engine, Analytics service, Synthetic data generator
│   ├── tests/              # Pytest automated test suites
│   ├── main.py             # FastAPI entrypoint
│   └── requirements.txt
├── live-app/               # 1-Click Netlify-ready full executive application
│   ├── index.html
│   └── _redirects
├── docs/                   # Complete BRD, FRD, Architecture ERD, Interview Demo Script
├── .env.example
├── .gitignore
└── README.md
```

---

## License
MIT License. Open-source enterprise portfolio platform.
