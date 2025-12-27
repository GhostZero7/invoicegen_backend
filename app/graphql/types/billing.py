import strawberry
from typing import List, Optional
from datetime import datetime
from app.db.models.user import SubscriptionPlan, SubscriptionStatus

@strawberry.type
class BillingPlanType:
    id: str
    name: str
    plan_type: SubscriptionPlan
    description: Optional[str]
    price_monthly: float
    price_yearly: float
    currency: str
    max_invoices_per_month: Optional[int]
    max_businesses: Optional[int]
    features: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

@strawberry.type
class SubscriptionType:
    id: str
    user_id: str
    plan: BillingPlanType
    status: SubscriptionStatus
    stripe_subscription_id: Optional[str]
    stripe_customer_id: Optional[str]
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    cancel_at_period_end: bool
    created_at: datetime
    updated_at: datetime
