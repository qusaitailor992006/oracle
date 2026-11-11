# System Architecture & Relational Schema (ERD)
## Project: ORACLE — Autonomous Decision Intelligence Engine

---

### High-Level Architecture Flow

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

### Relational Entity-Relationship Diagram (ERD)

```
┌─────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│   departments   │       │    customers    │       │     products     │
├─────────────────┤       ├─────────────────┤       ├──────────────────┤
│ id (PK)         │◄──┐   │ id (PK)         │◄──┐   │ id (PK)          │◄──┐
│ name            │   │   │ name            │   │   │ name             │   │
│ annual_budget   │   │   │ segment         │   │   │ category         │   │
│ head_count      │   │   │ churn_risk      │   │   │ unit_cost        │   │
│ manager_name    │   │   │ lifetime_value  │   │   │ unit_price       │   │
└─────────────────┘   │   └─────────────────┘   │   │ margin_percent   │   │
                      │                         │   └──────────────────┘   │
┌─────────────────┐   │   ┌─────────────────┐   │                          │
│department_exp   │   │   │     orders      │   │   ┌──────────────────┐   │
├─────────────────┤   │   ├─────────────────┤   │   │   order_items    │   │
│ id (PK)         │   │   │ id (PK)         │◄──┼───┤ id (PK)          │   │
│ department_id   ├───┘   │ customer_id     ├───┘   │ order_id         ├───┘
│ year, month     │       │ total_amount    │       │ product_id       │
│ amount, budget  │       │ channel         │       │ quantity, total  │
│ variance        │       └─────────────────┘       └──────────────────┘
└─────────────────┘
```
