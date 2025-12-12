import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.db.models.invoice import Invoice as InvoiceModel, InvoiceItem as InvoiceItemModel
from app.db.models.business import BusinessProfile

@strawberry.type
class InvoiceQuery:
    @strawberry.field
    async def invoice(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Invoice]:
        """Get a specific invoice by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            return None
        
        return Invoice(
            id=strawberry.ID(str(invoice.id)),
            business_id=strawberry.ID(str(invoice.business_id)),
            client_id=strawberry.ID(str(invoice.client_id)),
            invoice_number=invoice.invoice_number,
            reference_number=invoice.reference_number,
            purchase_order_number=invoice.purchase_order_number,
            status=invoice.status,
            invoice_date=invoice.invoice_date,
            due_date=invoice.due_date,
            payment_terms=invoice.payment_terms.value,
            subtotal=invoice.subtotal,
            discount_type=invoice.discount_type,
            discount_value=invoice.discount_value,
            discount_amount=invoice.discount_amount,
            tax_amount=invoice.tax_amount,
            shipping_amount=invoice.shipping_amount,
            total_amount=invoice.total_amount,
            amount_paid=invoice.amount_paid,
            amount_due=invoice.amount_due,
            currency=invoice.currency,
            notes=invoice.notes,
            payment_instructions=invoice.payment_instructions,
            footer_text=invoice.footer_text,
            is_recurring=invoice.is_recurring,
            sent_at=invoice.sent_at,
            viewed_at=invoice.viewed_at,
            paid_at=invoice.paid_at,
            cancelled_at=invoice.cancelled_at,
            created_at=invoice.created_at,
            updated_at=invoice.updated_at
        )
    
    @strawberry.field
    async def invoices(
        self,
        info: strawberry.Info,
        business_id: Optional[strawberry.ID] = None,
        client_id: Optional[strawberry.ID] = None,
        status: Optional[InvoiceStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Invoice]:
        """Get invoices with optional filters"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        query = db.query(InvoiceModel).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id
        )
        
        if business_id:
            query = query.filter(InvoiceModel.business_id == str(business_id))
        
        if client_id:
            query = query.filter(InvoiceModel.client_id == str(client_id))
        
        if status:
            query = query.filter(InvoiceModel.status == status.value)
        
        invoices = query.offset(skip).limit(limit).all()
        
        return [Invoice(
            id=strawberry.ID(str(inv.id)),
            business_id=strawberry.ID(str(inv.business_id)),
            client_id=strawberry.ID(str(inv.client_id)),
            invoice_number=inv.invoice_number,
            reference_number=inv.reference_number,
            purchase_order_number=inv.purchase_order_number,
            status=inv.status,
            invoice_date=inv.invoice_date,
            due_date=inv.due_date,
            payment_terms=inv.payment_terms.value,
            subtotal=inv.subtotal,
            discount_type=inv.discount_type,
            discount_value=inv.discount_value,
            discount_amount=inv.discount_amount,
            tax_amount=inv.tax_amount,
            shipping_amount=inv.shipping_amount,
            total_amount=inv.total_amount,
            amount_paid=inv.amount_paid,
            amount_due=inv.amount_due,
            currency=inv.currency,
            notes=inv.notes,
            payment_instructions=inv.payment_instructions,
            footer_text=inv.footer_text,
            is_recurring=inv.is_recurring,
            sent_at=inv.sent_at,
            viewed_at=inv.viewed_at,
            paid_at=inv.paid_at,
            cancelled_at=inv.cancelled_at,
            created_at=inv.created_at,
            updated_at=inv.updated_at
        ) for inv in invoices]
    
    @strawberry.field
    async def invoice_items(self, info: strawberry.Info, invoice_id: strawberry.ID) -> List[InvoiceItem]:
        """Get all items for a specific invoice"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business that owns this invoice
        items = db.query(InvoiceItemModel).join(
            InvoiceModel, InvoiceItemModel.invoice_id == InvoiceModel.id
        ).join(BusinessProfile).filter(
            InvoiceItemModel.invoice_id == str(invoice_id),
            BusinessProfile.user_id == user.id
        ).order_by(InvoiceItemModel.sort_order).all()
        
        return [InvoiceItem(
            id=strawberry.ID(str(item.id)),
            invoice_id=strawberry.ID(str(item.invoice_id)),
            product_id=strawberry.ID(str(item.product_id)) if item.product_id else None,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            unit_of_measure=item.unit_of_measure,
            tax_rate=item.tax_rate,
            tax_amount=item.tax_amount,
            discount_type=item.discount_type,
            discount_value=item.discount_value,
            discount_amount=item.discount_amount,
            line_total=item.line_total,
            sort_order=item.sort_order
        ) for item in items]
