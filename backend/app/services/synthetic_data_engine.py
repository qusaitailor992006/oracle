import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from backend.app.models.oracle_models import (
    Department, Employee, Customer, Product, Order, OrderItem,
    FinancialRecord, DepartmentExpense, InvestigationCase, QueryAuditLog
)

fake = Faker()
Faker.seed(101)
random.seed(101)

DEPARTMENTS_CONFIG = [
    ("Engineering & Cloud", "ENG", 6500000.0, 45, "Dr. Aris Thorne"),
    ("Global Sales & Partnerships", "SALES", 4800000.0, 32, "Victoria Sterling"),
    ("Growth & Performance Marketing", "MKTG", 3600000.0, 20, "Julian Vance"),
    ("Customer Success & Support", "CS", 2200000.0, 28, "Nadia Al-Mansoor"),
    ("General & Operations", "OPS", 1900000.0, 15, "Marcus Bradley")
]

PRODUCTS_CONFIG = [
    ("Cloud Analytics Platform (Tier 1)", "Cloud Infra", 450.0, 1850.0),
    ("Enterprise Decision Suite", "Enterprise Software", 800.0, 4200.0),
    ("Real-Time Telemetry Pipeline", "Cloud Infra", 350.0, 1450.0),
    ("Automated Compliance Scanner", "Security", 250.0, 950.0),
    ("Predictive ML Inference Engine", "Analytics Suite", 600.0, 2800.0),
    ("Executive BI Looker Connector", "Analytics Suite", 150.0, 750.0),
    ("Architecture Consulting (Monthly)", "Consulting", 2800.0, 5000.0),
    ("Dedicated Support SLA (Gold)", "Support", 400.0, 1200.0)
]

class SyntheticBusinessDataEngine:
    def seed_initial_enterprise_data(self, db: Session):
        if db.query(Department).count() > 0:
            return # Already seeded
            
        # 1. Departments
        departments = []
        for name, code, budget, hc, mgr in DEPARTMENTS_CONFIG:
            dept = Department(
                name=name,
                code=code,
                annual_budget=budget,
                head_count=hc,
                manager_name=mgr
            )
            departments.append(dept)
        db.add_all(departments)
        db.commit()

        # 2. Employees
        employees = []
        for dept in departments:
            for _ in range(8):
                emp = Employee(
                    name=fake.name(),
                    email=fake.unique.company_email(),
                    department_id=dept.id,
                    salary=round(random.uniform(75000, 185000), -2),
                    role=fake.job(),
                    performance_score=round(random.uniform(3.2, 4.9), 1),
                    hire_date=datetime.utcnow() - timedelta(days=random.randint(60, 1200))
                )
                employees.append(emp)
        db.add_all(employees)
        db.commit()

        # 3. Products
        products = []
        for idx, (name, cat, cost, price) in enumerate(PRODUCTS_CONFIG):
            margin = round(((price - cost) / price) * 100, 1)
            prod = Product(
                id=f"PROD-{100 + idx}",
                name=name,
                category=cat,
                unit_cost=cost,
                unit_price=price,
                margin_percent=margin,
                status="active"
            )
            products.append(prod)
        db.add_all(products)
        db.commit()

        # 4. Customers
        customers = []
        segments = ["Enterprise", "Mid-Market", "SMB"]
        segment_weights = [0.2, 0.35, 0.45]
        
        for i in range(120):
            seg = random.choices(segments, weights=segment_weights)[0]
            signup = datetime.utcnow() - timedelta(days=random.randint(30, 720))
            churn_risk = round(random.betavariate(2, 5) * 100, 1)
            status = "churned" if churn_risk > 80 and random.random() < 0.6 else ("at_risk" if churn_risk > 65 else "active")
            
            cust = Customer(
                id=f"CUST-{1000 + i}",
                name=fake.company(),
                email=fake.company_email(),
                segment=seg,
                country=random.choice(["US", "US", "US", "GB", "DE", "CA", "SG"]),
                signup_date=signup,
                churn_risk_score=churn_risk,
                lifetime_value=0.0,
                status=status
            )
            customers.append(cust)
        db.add_all(customers)
        db.commit()

        # 5. Orders & Order Items (Last 12 Months)
        orders = []
        order_items = []
        now = datetime.utcnow()
        
        for cust in customers:
            # Generate 1 to 8 orders per customer based on segment
            num_orders = random.randint(4, 10) if cust.segment == "Enterprise" else (random.randint(2, 5) if cust.segment == "Mid-Market" else random.randint(1, 3))
            cust_total_spend = 0.0
            
            for o_idx in range(num_orders):
                order_date = cust.signup_date + timedelta(days=random.randint(5, 300))
                if order_date > now:
                    order_date = now - timedelta(days=random.randint(1, 45))
                    
                order_id = f"ORD-{random.randint(100000, 999999)}"
                chosen_product = random.choice(products)
                qty = random.randint(1, 5) if cust.segment == "Enterprise" else random.randint(1, 2)
                line_total = round(chosen_product.unit_price * qty, 2)
                discount = round(line_total * random.choice([0.0, 0.05, 0.10]), 2)
                order_total = round(line_total - discount, 2)
                cust_total_spend += order_total

                ord_item = OrderItem(
                    order_id=order_id,
                    product_id=chosen_product.id,
                    quantity=qty,
                    unit_price=chosen_product.unit_price,
                    line_total=line_total,
                    profit_margin=chosen_product.margin_percent
                )
                order_items.append(ord_item)

                ord_obj = Order(
                    id=order_id,
                    customer_id=cust.id,
                    order_date=order_date,
                    total_amount=order_total,
                    discount_amount=discount,
                    payment_status="completed",
                    channel=random.choice(["Direct Sales", "Online Portal", "Channel Partner"])
                )
                orders.append(ord_obj)
                
            cust.lifetime_value = round(cust_total_spend, 2)

        db.add_all(orders)
        db.add_all(order_items)
        db.commit()

        # 6. Monthly Financial Records (P&L for past 24 months)
        financial_records = []
        base_revenue = 680000.0
        
        for m in range(24):
            # calculate year and month backwards
            dt = now - timedelta(days=(24 - m) * 30.5)
            yr = dt.year
            mo = dt.month
            q = f"Q{((mo - 1) // 3) + 1}"
            
            # Growth trend + seasonal variations
            growth_factor = 1.0 + (m * 0.025) # healthy 2.5% monthly compound growth
            seasonal = 1.15 if mo in [11, 12] else (0.92 if mo in [7, 8] else 1.0)
            rev = round(base_revenue * growth_factor * seasonal + random.uniform(-15000, 20000), 2)
            cogs = round(rev * random.uniform(0.24, 0.28), 2)
            gross = round(rev - cogs, 2)
            
            # Q3 marketing spike simulation in 2025
            mktg_spike = 45000.0 if (mo in [8, 9] and yr == 2025) else 0.0
            opex = round((rev * 0.42) + mktg_spike + random.uniform(10000, 25000), 2)
            net = round(gross - opex, 2)
            ebitda = round(net + (opex * 0.12), 2)
            cash_flow = round(net * random.uniform(0.85, 1.15), 2)
            burn = 0.0 if net > 0 else abs(net)

            rec = FinancialRecord(
                year=yr,
                quarter=q,
                month=mo,
                revenue=rev,
                cogs=cogs,
                gross_profit=gross,
                operating_expenses=opex,
                net_profit=net,
                ebitda=ebitda,
                cash_flow=cash_flow,
                burn_rate=burn
            )
            financial_records.append(rec)
        db.add_all(financial_records)
        db.commit()

        # 7. Department Expenses (Past 6 Months)
        dept_expenses = []
        for dept in departments:
            monthly_budget = round(dept.annual_budget / 12, 2)
            for mo in range(1, 7):
                # Simulate overspend in Marketing
                variance_mult = random.uniform(1.10, 1.25) if (dept.code == "MKTG" and mo in [4, 5]) else random.uniform(0.92, 1.04)
                actual_spent = round(monthly_budget * variance_mult, 2)
                var = round(actual_spent - monthly_budget, 2)

                exp = DepartmentExpense(
                    department_id=dept.id,
                    year=2026,
                    month=mo,
                    category="Payroll & Operations" if dept.code != "MKTG" else "Paid Acquisition & Brand Campaigns",
                    amount=actual_spent,
                    budget_allocated=monthly_budget,
                    variance=var
                )
                dept_expenses.append(exp)
        db.add_all(dept_expenses)
        db.commit()

        # 8. Seed Pre-built High-Impact Investigation Cases
        case_1 = InvestigationCase(
            id="INV-2026-001",
            title="Q3 Operating Expense Variance & Marketing Overrun Root Cause",
            user_query="Why did operating expenses exceed budget in Q3, and what was the net impact on margins?",
            status="ACTION_PENDING",
            department="Growth & Performance Marketing",
            hypothesis="Uncapped performance acquisition campaigns during product launch led to a $95k budget variance with diminishing return on ad spend (ROAS).",
            findings=[
                "Marketing department exceeded allocated Q3 budget by $92,400 (23.4% variance).",
                "Customer Acquisition Cost (CAC) rose from $320 to $540 for SMB segment.",
                "Gross margins remained stable at 74.2%, but Net Margin compressed from 18.2% to 11.4%."
            ],
            generated_sql="SELECT department_id, SUM(amount) as total_spent, SUM(budget_allocated) as total_budget, SUM(variance) as overrun FROM department_expenses WHERE department_id = 3 GROUP BY department_id;",
            evidence_data={"budget": 300000, "actual": 392400, "overrun": 92400, "roas_drop": "-28%"},
            recommendation="Cap automated campaign ad spend at $65,000/month; reallocate 35% of growth budget into Enterprise Account-Based Marketing (ABM) which shows 3.8x higher LTV.",
            estimated_impact_usd=145000.0,
            confidence_score=92.5,
            human_approved=False
        )

        case_2 = InvestigationCase(
            id="INV-2026-002",
            title="Enterprise Customer Cohort Churn Risk & Retention Opportunity",
            user_query="Which customer accounts are at critical churn risk and what recurring revenue is exposed?",
            status="RESOLVED",
            department="Customer Success & Support",
            hypothesis="Five legacy enterprise accounts show usage drop-offs of >40% post-migration to Cloud Analytics Tier 1.",
            findings=[
                "14 enterprise and mid-market accounts currently flagged with churn risk scores > 70.",
                "Total Annual Recurring Revenue (ARR) exposed: $284,500.",
                "Root cause identified: Lack of executive onboarding support and unresolved API latency tickets."
            ],
            generated_sql="SELECT id, name, segment, churn_risk_score, lifetime_value FROM customers WHERE churn_risk_score >= 70 AND segment IN ('Enterprise', 'Mid-Market') ORDER BY lifetime_value DESC;",
            evidence_data={"at_risk_accounts": 14, "arr_exposure": 284500, "top_account": "Vance Logistics ($42k ARR)"},
            recommendation="Deploy dedicated Technical Account Managers (TAM) to top 5 at-risk accounts; offer 2 months complimentary Gold SLA support during optimization.",
            estimated_impact_usd=210000.0,
            confidence_score=94.0,
            human_approved=True
        )

        db.add_all([case_1, case_2])
        db.commit()

synthetic_business_engine = SyntheticBusinessDataEngine()
