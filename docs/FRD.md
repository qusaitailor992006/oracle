# Functional Requirements Document (FRD)
## Project: ORACLE — Autonomous Enterprise Decision Intelligence Engine

---

### 1. Natural Language Business Query Engine
- **FR-1.1**: The system shall accept arbitrary business questions in plain English via a search interface.
- **FR-1.2**: The engine shall synthesize intent into valid SQL statements targeting `financial_records`, `departments`, `department_expenses`, `customers`, and `products`.
- **FR-1.3**: The engine shall strictly enforce read-only execution: rejecting any query containing `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, or `PRAGMA`.
- **FR-1.4**: Output responses shall include:
  1. Plain-English executive synthesis.
  2. Structured tabular data with column sorting.
  3. Evidence-backed bulleted insights.
  4. Prescribed next business action.
  5. Calculation confidence score (0-100%).

---

### 2. Financial & Business Analytics Module
- **FR-2.1**: The system shall compute Annual Recurring Revenue (`ARR = MRR * 12`), Gross Profit Margin (`(Gross / Revenue) * 100`), Net Profit Margin, and EBITDA.
- **FR-2.2**: The platform shall track historical monthly P&L records for trailing 12 and 24-month periods.
- **FR-2.3**: Departmental budgets shall calculate actual expenditure vs budget allocation and flag positive variance overruns.

---

### 3. Automated Investigation & Recommendation Engine
- **FR-3.1**: The system shall maintain distinct `InvestigationCase` records capturing hypothesis, analytical findings, generated SQL, and estimated financial impact ($ USD).
- **FR-3.2**: Recommended interventions shall require explicit human authorization (`human_approved = true/false`) before state transitions to `RESOLVED`.

---

### 4. Security & Audit Logging
- **FR-4.1**: Every executed query shall generate an immutable `QueryAuditLog` entry capturing user email, query string, generated SQL, execution duration in milliseconds, and row count.
- **FR-4.2**: The system shall enforce prompt injection defenses, preventing prompt leaks and jailbreak attacks.
