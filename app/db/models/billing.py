from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base
from app.db.models.user import SubscriptionPlan, SubscriptionStatus

class BillingPlan(Base):
    __tablename__ = "billing_plans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    plan_type = Column(Enum(SubscriptionPlan), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    price_monthly = Column(Float, default=0.0)
    price_yearly = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    
    # Limits and Features
    max_invoices_per_month = Column(Integer, nullable=True)  # NULL for unlimited
    max_businesses = Column(Integer, nullable=True)         # NULL for unlimited
    features = Column(JSON, default=list)                   # List of feature keys
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    plan_id = Column(String, ForeignKey("billing_plans.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    
    # Stripe integration bits
    stripe_subscription_id = Column(String(255), nullable=True, index=True)
    stripe_customer_id = Column(String(255), nullable=True, index=True)
    
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscription")
    plan = relationship("BillingPlan", back_populates="subscriptions")
