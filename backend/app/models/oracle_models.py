from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) # Engineering, Sales, Marketing, Operations, Finance
    code = Column(String(20), unique=True, nullable=False)
    annual_budget = Column(Float, nullable=False)
    head_count = Column(Integer, default=10)
    manager_name = Column(String(100))
    
    employees = relationship("Employee", back_populates="department")
    expenses = relationship("DepartmentExpense", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    salary = Column(Float, nullable=False)
    role = Column(String(100))
    performance_score = Column(Float, default=4.0) # 1.0 to 5.0
    hire_date = Column(DateTime, default=datetime.utcnow)
    
    department = relationship("Department", back_populates="employees")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. CUST-10492
    name = Column(String(150), nullable=False)
    email = Column(String(150))
    segment = Column(String(50), default="SMB") # Enterprise, Mid-Market, SMB
    country = Column(String(10), default="US")
    signup_date = Column(DateTime, default=datetime.utcnow)
    churn_risk_score = Column(Float, default=15.0) # 0 to 100
    lifetime_value = Column(Float, default=0.0)
    status = Column(String(50), default="active") # active, at_risk, churned
    
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. PROD-802
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False) # Cloud Infra, Enterprise Software, Analytics Suite, Consulting
    unit_cost = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    margin_percent = Column(Float, nullable=False)
    status = Column(String(50), default="active")
    
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. ORD-2026-9041
    customer_id = Column(String(64), ForeignKey("customers.id"), nullable=False, index=True)
    order_date = Column(DateTime, default=datetime.utcnow, index=True)
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    payment_status = Column(String(50), default="completed") # completed, pending, refunded
    channel = Column(String(50), default="Direct Sales") # Direct Sales, Online, Partner
    
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(64), ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(String(64), ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    profit_margin = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class FinancialRecord(Base):
    __tablename__ = "financial_records"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(String(10), nullable=False) # Q1, Q2, Q3, Q4
    month = Column(Integer, nullable=False, index=True) # 1 to 12
    revenue = Column(Float, nullable=False)
    cogs = Column(Float, nullable=False) # Cost of Goods Sold
    gross_profit = Column(Float, nullable=False)
    operating_expenses = Column(Float, nullable=False)
    net_profit = Column(Float, nullable=False)
    ebitda = Column(Float, nullable=False)
    cash_flow = Column(Float, nullable=False)
    burn_rate = Column(Float, default=0.0)

class DepartmentExpense(Base):
    __tablename__ = "department_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False) # Payroll, Software/Cloud, Marketing Ads, Travel, Consulting
    amount = Column(Float, nullable=False)
    budget_allocated = Column(Float, nullable=False)
    variance = Column(Float, nullable=False) # amount - budget_allocated (positive = overrun)
    
    department = relationship("Department", back_populates="expenses")

class InvestigationCase(Base):
    __tablename__ = "investigation_cases"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. INV-2026-001
    title = Column(String(255), nullable=False)
    user_query = Column(Text, nullable=False)
    status = Column(String(50), default="COMPLETED") # ANALYZING, COMPLETED, ACTION_PENDING, RESOLVED
    department = Column(String(100))
    hypothesis = Column(Text)
    findings = Column(JSON, default=list) # List of key analytical findings
    generated_sql = Column(Text)
    evidence_data = Column(JSON, default=dict)
    recommendation = Column(Text)
    estimated_impact_usd = Column(Float, default=0.0)
    confidence_score = Column(Float, default=85.0)
    human_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class QueryAuditLog(Base):
    __tablename__ = "query_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(150), default="executive@oracle.internal")
    natural_language_query = Column(Text, nullable=False)
    executed_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Float, default=0.0)
    row_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
