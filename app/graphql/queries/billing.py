import strawberry
from typing import List, Optional
from strawberry.types import Info
from app.graphql.types.billing import BillingPlanType, SubscriptionType
from app.db.models.billing import BillingPlan, Subscription
from app.db.database import SessionLocal

@strawberry.type
class BillingQuery:
    @strawberry.field
    def available_plans(self, info: Info) -> List[BillingPlanType]:
        db = info.context.get("db")
        plans = db.query(BillingPlan).filter(BillingPlan.is_active == True).all()
        return [
            BillingPlanType(
                id=p.id,
                name=p.name,
                plan_type=p.plan_type,
                description=p.description,
                price_monthly=p.price_monthly,
                price_yearly=p.price_yearly,
                currency=p.currency,
                max_invoices_per_month=p.max_invoices_per_month,
                max_businesses=p.max_businesses,
                features=p.features,
                is_active=p.is_active,
                created_at=p.created_at,
                updated_at=p.updated_at
            ) for p in plans
        ]

    @strawberry.field
    def current_subscription(self, info: Info) -> Optional[SubscriptionType]:
        user = info.context.get("user")
        if not user:
            return None
            
        db = info.context.get("db")
        subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
        
        if not subscription:
            return None
            
        return SubscriptionType(
            id=subscription.id,
            user_id=subscription.user_id,
            plan=BillingPlanType(
                id=subscription.plan.id,
                name=subscription.plan.name,
                plan_type=subscription.plan.plan_type,
                description=subscription.plan.description,
                price_monthly=subscription.plan.price_monthly,
                price_yearly=subscription.plan.price_yearly,
                currency=subscription.plan.currency,
                max_invoices_per_month=subscription.plan.max_invoices_per_month,
                max_businesses=subscription.plan.max_businesses,
                features=subscription.plan.features,
                is_active=subscription.plan.is_active,
                created_at=subscription.plan.created_at,
                updated_at=subscription.plan.updated_at
            ),
            status=subscription.status,
            stripe_subscription_id=subscription.stripe_subscription_id,
            stripe_customer_id=subscription.stripe_customer_id,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            created_at=subscription.created_at,
            updated_at=subscription.updated_at
        )
