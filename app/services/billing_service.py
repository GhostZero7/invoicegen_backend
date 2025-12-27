from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.models.user import User, SubscriptionPlan, SubscriptionStatus
from app.db.models.business import BusinessProfile
from app.db.models.invoice import Invoice
from app.db.models.billing import BillingPlan, Subscription

PLAN_LIMITS = {
    SubscriptionPlan.FREE: {
        "max_invoices_per_month": 5,
        "max_businesses": 1,
        "features": ["basic_pdf"]
    },
    SubscriptionPlan.STARTER: {
        "max_invoices_per_month": 50,
        "max_businesses": 2,
        "features": ["custom_branding", "reminders"]
    },
    SubscriptionPlan.PRO: {
        "max_invoices_per_month": float('inf'),
        "max_businesses": 5,
        "features": ["custom_branding", "reminders", "recurring_invoices", "advanced_reporting"]
    },
    SubscriptionPlan.ENTERPRISE: {
        "max_invoices_per_month": float('inf'),
        "max_businesses": float('inf'),
        "features": ["custom_branding", "reminders", "recurring_invoices", "advanced_reporting", "audit_logs", "priority_support"]
    }
}

class BillingService:
    @staticmethod
    def get_active_subscription(db: Session, user_id: str):
        """Get the user's active subscription with its plan details."""
        return db.query(Subscription).options(
            joinedload(Subscription.plan)
        ).filter(Subscription.user_id == user_id).first()

    @staticmethod
    def get_user_plan(db: Session, user_id: str):
        subscription = BillingService.get_active_subscription(db, user_id)
        if subscription:
            return subscription.plan.plan_type, subscription.status
            
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return SubscriptionPlan.FREE, SubscriptionStatus.CANCELED
        return user.subscription_plan, user.subscription_status

    @staticmethod
    def get_plan_limits(db: Session, user_id: str):
        """Helper to get plan limits, either from DB or fallback dictionary."""
        subscription = BillingService.get_active_subscription(db, user_id)
        if subscription and subscription.plan:
            plan = subscription.plan
            return {
                "max_invoices_per_month": plan.max_invoices_per_month or float('inf'),
                "max_businesses": plan.max_businesses or float('inf'),
                "features": plan.features or []
            }
        
        # Fallback to User model fields and hardcoded limits
        user = db.query(User).filter(User.id == user_id).first()
        plan_type = user.subscription_plan if user else SubscriptionPlan.FREE
        return PLAN_LIMITS.get(plan_type, PLAN_LIMITS[SubscriptionPlan.FREE])

    @staticmethod
    def can_create_invoice(db: Session, business_id: str) -> bool:
        business = db.query(BusinessProfile).filter(BusinessProfile.id == business_id).first()
        if not business:
            return False
        
        user_id = business.user_id
        subscription = BillingService.get_active_subscription(db, user_id)
        
        # Check status
        status = subscription.status if subscription else None
        if not status:
            user = db.query(User).filter(User.id == user_id).first()
            status = user.subscription_status if user else SubscriptionStatus.CANCELED

        if status not in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]:
            return False
            
        limits = BillingService.get_plan_limits(db, user_id)
        limit = limits["max_invoices_per_month"]
        
        if limit == float('inf'):
            return True
            
        # Count invoices created this month
        first_day_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        count = db.query(func.count(Invoice.id)).filter(
            Invoice.business_id == business_id,
            Invoice.created_at >= first_day_of_month
        ).scalar()
        
        return count < limit

    @staticmethod
    def can_create_business(db: Session, user_id: str) -> bool:
        limits = BillingService.get_plan_limits(db, user_id)
        limit = limits["max_businesses"]
        
        if limit == float('inf'):
            return True
            
        count = db.query(func.count(BusinessProfile.id)).filter(
            BusinessProfile.user_id == user_id,
            BusinessProfile.is_active == True
        ).scalar()
        
        return count < limit

    @staticmethod
    def has_feature(db: Session, user_id: str, feature_name: str) -> bool:
        limits = BillingService.get_plan_limits(db, user_id)
        return feature_name in (limits.get("features") or [])
