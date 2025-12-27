import strawberry
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.graphql.types.invoice import Invoice, CreateInvoiceInput, UpdateInvoiceInput
from app.db.models.invoice import Invoice as InvoiceModel, InvoiceItem as InvoiceItemModel
from app.db.models.business import BusinessProfile
from app.services.billing_service import BillingService

@strawberry.type
class InvoiceMutation:
    @strawberry.mutation
    async def create_invoice(self, info: strawberry.Info, input: CreateInvoiceInput) -> Invoice:
        """Create a new invoice with items"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
            
        # Check billing limits
        if not BillingService.can_create_invoice(db, str(input.business_id)):
            raise Exception("Monthly invoice limit reached for your plan. Please upgrade to create more invoices.")
        
        # Verify user owns the business
        business = db.query(BusinessProfile).filter(
            BusinessProfile.id == str(input.business_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        # Generate invoice number
        invoice_number = f"{business.invoice_prefix}-{business.next_invoice_number:05d}"
        business.next_invoice_number += 1
        
        # Calculate totals
        subtotal = 0.0
        tax_amount = 0.0
        
        for item_input in input.items:
            item_subtotal = item_input.quantity * item_input.unit_price
            item_discount = 0.0
            
            if item_input.discount_type and item_input.discount_value:
                if item_input.discount_type.value == "percentage":
                    item_discount = item_subtotal * (item_input.discount_value / 100)
                else:
                    item_discount = item_input.discount_value
            
            item_after_discount = item_subtotal - item_discount
            item_tax = item_after_discount * ((item_input.tax_rate or 0.0) / 100)
            
            subtotal += item_subtotal
            tax_amount += item_tax
        
        discount_amount = 0.0
        if input.discount_type and input.discount_value:
            if input.discount_type.value == "percentage":
                discount_amount = subtotal * (input.discount_value / 100)
            else:
                discount_amount = input.discount_value
        
        total_amount = subtotal - discount_amount + tax_amount + (input.shipping_amount or 0.0)
        
        invoice = InvoiceModel(
            id=str(uuid.uuid4()),
            business_id=str(input.business_id),
            client_id=str(input.client_id),
            invoice_number=invoice_number,
            status="draft",
            invoice_date=input.invoice_date.date(),
            due_date=input.due_date.date(),
            payment_terms=input.payment_terms,
            subtotal=subtotal,
            discount_type=input.discount_type.value if input.discount_type else None,
            discount_value=input.discount_value or 0.0,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            shipping_amount=input.shipping_amount or 0.0,
            total_amount=total_amount,
            amount_paid=0.0,
            amount_due=total_amount,
            currency=business.currency,
            notes=input.notes,
            payment_instructions=input.payment_instructions,
            created_by=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(invoice)
        db.flush()
        
        # Create invoice items
        for idx, item_input in enumerate(input.items):
            item_subtotal = item_input.quantity * item_input.unit_price
            item_discount = 0.0
            
            if item_input.discount_type and item_input.discount_value:
                if item_input.discount_type.value == "percentage":
                    item_discount = item_subtotal * (item_input.discount_value / 100)
                else:
                    item_discount = item_input.discount_value
            
            item_after_discount = item_subtotal - item_discount
            item_tax = item_after_discount * ((item_input.tax_rate or 0.0) / 100)
            line_total = item_after_discount + item_tax
            
            item = InvoiceItemModel(
                id=str(uuid.uuid4()),
                invoice_id=invoice.id,
                product_id=str(item_input.product_id) if item_input.product_id else None,
                description=item_input.description,
                quantity=item_input.quantity,
                unit_price=item_input.unit_price,
                unit_of_measure=item_input.unit_of_measure or "unit",
                tax_rate=item_input.tax_rate or 0.0,
                tax_amount=item_tax,
                discount_type=item_input.discount_type.value if item_input.discount_type else None,
                discount_value=item_input.discount_value or 0.0,
                discount_amount=item_discount,
                line_total=line_total,
                sort_order=idx,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(item)
        
        db.commit()
        db.refresh(invoice)
        
        return Invoice(
            id=strawberry.ID(str(invoice.id)),
            business_id=strawberry.ID(str(invoice.business_id)),
            client_id=strawberry.ID(str(invoice.client_id)),
            client=Client(
                id=strawberry.ID(str(client.id)),
                business_id=strawberry.ID(str(client.business_id)),
                first_name=client.first_name,
                last_name=client.last_name,
                status=client.status,
                phone=client.phone,
                email=client.email,
                notes=client.notes,
                company_name=client.company_name,
                created_at=client.created_at,
                updated_at=client.updated_at,
                client_type=client.client_type,
                mobile=client.mobile,
                website=client.website,
                tax_id=client.tax_id,
                vat_number=client.vat_number,
                payment_terms=client.payment_terms,
                credit_limit=client.credit_limit,
                currency=client.currency,
                language=client.language 
            ),
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
    
    @strawberry.mutation
    async def update_invoice(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdateInvoiceInput
    ) -> Invoice:
        """Update an existing invoice"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            raise Exception("Invoice not found")
        
        if input.status is not None:
            invoice.status = input.status.value
        if input.due_date is not None:
            invoice.due_date = input.due_date.date()
        if input.notes is not None:
            invoice.notes = input.notes
        if input.payment_instructions is not None:
            invoice.payment_instructions = input.payment_instructions
        
        invoice.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(invoice)
        
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
    
    @strawberry.mutation
    async def delete_invoice(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete an invoice"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            raise Exception("Invoice not found")
        
        db.delete(invoice)
        db.commit()
        
        return True
    
    @strawberry.mutation
    async def send_invoice(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Mark invoice as sent"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            raise Exception("Invoice not found")
        
        invoice.status = "sent"
        invoice.sent_at = datetime.utcnow()
        invoice.updated_at = datetime.utcnow()
        
        db.commit()
        
        return True
    
    @strawberry.mutation
    async def mark_invoice_as_paid(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Mark invoice as paid"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            raise Exception("Invoice not found")
        
        invoice.status = "paid"
        invoice.paid_at = datetime.utcnow()
        invoice.amount_paid = invoice.total_amount
        invoice.amount_due = 0.0
        invoice.updated_at = datetime.utcnow()
        
        db.commit()
        
        return True
    
    @strawberry.mutation
    async def cancel_invoice(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Cancel an invoice"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            raise Exception("Invoice not found")
        
        invoice.status = "cancelled"
        invoice.cancelled_at = datetime.utcnow()
        invoice.updated_at = datetime.utcnow()
        
        db.commit()
        
        return True
