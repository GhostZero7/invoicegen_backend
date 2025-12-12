import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.payment import Payment, PaymentStatus
from app.db.models.payment import Payment as PaymentModel
from app.db.models.invoice import Invoice
from app.db.models.business import BusinessProfile

@strawberry.type
class PaymentQuery:
    @strawberry.field
    async def payment(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Payment]:
        """Get a specific payment by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        payment = db.query(PaymentModel).join(
            Invoice, PaymentModel.invoice_id == Invoice.id
        ).join(BusinessProfile).filter(
            PaymentModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not payment:
            return None
        
        return Payment(
            id=strawberry.ID(str(payment.id)),
            invoice_id=strawberry.ID(str(payment.invoice_id)),
            payment_number=payment.payment_number,
            payment_date=payment.payment_date,
            amount=payment.amount,
            payment_method=payment.payment_method,
            transaction_id=payment.transaction_id,
            reference_number=payment.reference_number,
            notes=payment.notes,
            status=payment.status,
            created_at=payment.created_at,
            updated_at=payment.updated_at
        )
    
    @strawberry.field
    async def payments(
        self,
        info: strawberry.Info,
        invoice_id: Optional[strawberry.ID] = None,
        status: Optional[PaymentStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Payment]:
        """Get payments with optional filters"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        query = db.query(PaymentModel).join(
            Invoice, PaymentModel.invoice_id == Invoice.id
        ).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id
        )
        
        if invoice_id:
            query = query.filter(PaymentModel.invoice_id == str(invoice_id))
        
        if status:
            query = query.filter(PaymentModel.status == status.value)
        
        payments = query.offset(skip).limit(limit).all()
        
        return [Payment(
            id=strawberry.ID(str(p.id)),
            invoice_id=strawberry.ID(str(p.invoice_id)),
            payment_number=p.payment_number,
            payment_date=p.payment_date,
            amount=p.amount,
            payment_method=p.payment_method,
            transaction_id=p.transaction_id,
            reference_number=p.reference_number,
            notes=p.notes,
            status=p.status,
            created_at=p.created_at,
            updated_at=p.updated_at
        ) for p in payments]
