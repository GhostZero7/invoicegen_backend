import strawberry
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.graphql.types.payment import Payment, CreatePaymentInput, UpdatePaymentInput
from app.db.models.payment import Payment as PaymentModel
from app.db.models.invoice import Invoice
from app.db.models.business import BusinessProfile

@strawberry.type
class PaymentMutation:
    @strawberry.mutation
    async def create_payment(self, info: strawberry.Info, input: CreatePaymentInput) -> Payment:
        """Create a new payment"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business that owns the invoice
        invoice = db.query(Invoice).join(BusinessProfile).filter(
            Invoice.id == str(input.invoice_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            raise Exception("Invoice not found")
        
        # Generate payment number
        payment_number = f"PAY-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        payment = PaymentModel(
            id=str(uuid.uuid4()),
            invoice_id=str(input.invoice_id),
            payment_number=payment_number,
            payment_date=input.payment_date,
            amount=input.amount,
            payment_method=input.payment_method.value,
            transaction_id=input.transaction_id,
            reference_number=input.reference_number,
            notes=input.notes,
            status="completed",
            created_by=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(payment)
        
        # Update invoice amounts
        invoice.amount_paid += input.amount
        invoice.amount_due = invoice.total_amount - invoice.amount_paid
        
        if invoice.amount_due <= 0:
            invoice.status = "paid"
            invoice.paid_at = datetime.utcnow()
        
        invoice.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(payment)
        
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
    
    @strawberry.mutation
    async def update_payment(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdatePaymentInput
    ) -> Payment:
        """Update an existing payment"""
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
            raise Exception("Payment not found")
        
        old_amount = payment.amount
        
        if input.payment_date is not None:
            payment.payment_date = input.payment_date
        if input.amount is not None:
            payment.amount = input.amount
        if input.payment_method is not None:
            payment.payment_method = input.payment_method.value
        if input.transaction_id is not None:
            payment.transaction_id = input.transaction_id
        if input.reference_number is not None:
            payment.reference_number = input.reference_number
        if input.notes is not None:
            payment.notes = input.notes
        if input.status is not None:
            payment.status = input.status.value
        
        payment.updated_at = datetime.utcnow()
        
        # Update invoice if amount changed
        if input.amount is not None and input.amount != old_amount:
            invoice = db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
            if invoice:
                invoice.amount_paid = invoice.amount_paid - old_amount + payment.amount
                invoice.amount_due = invoice.total_amount - invoice.amount_paid
                
                if invoice.amount_due <= 0:
                    invoice.status = "paid"
                    invoice.paid_at = datetime.utcnow()
                elif invoice.status == "paid":
                    invoice.status = "sent"
                    invoice.paid_at = None
                
                invoice.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(payment)
        
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
    
    @strawberry.mutation
    async def delete_payment(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a payment"""
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
            raise Exception("Payment not found")
        
        # Update invoice amounts
        invoice = db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
        if invoice:
            invoice.amount_paid -= payment.amount
            invoice.amount_due = invoice.total_amount - invoice.amount_paid
            
            if invoice.status == "paid":
                invoice.status = "sent"
                invoice.paid_at = None
            
            invoice.updated_at = datetime.utcnow()
        
        db.delete(payment)
        db.commit()
        
        return True
    
    @strawberry.mutation
    async def refund_payment(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Refund a payment"""
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
            raise Exception("Payment not found")
        
        payment.status = "refunded"
        payment.updated_at = datetime.utcnow()
        
        # Update invoice amounts
        invoice = db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
        if invoice:
            invoice.amount_paid -= payment.amount
            invoice.amount_due = invoice.total_amount - invoice.amount_paid
            invoice.status = "refunded"
            invoice.updated_at = datetime.utcnow()
        
        db.commit()
        
        return True
