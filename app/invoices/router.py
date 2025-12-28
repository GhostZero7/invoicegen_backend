from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import SessionLocal
from app.db.models.invoice import Invoice, InvoiceItem
from app.db.models.business import BusinessProfile
from app.invoices.schemas import InvoiceCreate, InvoiceResponse, InvoiceUpdate, InvoiceListResponse
from app.core.deps import get_db, get_current_user
from app.db.models.user import User

router = APIRouter(tags=["Invoices"])

@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    invoice_in: InvoiceCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's business
    business = db.query(BusinessProfile).filter(BusinessProfile.user_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    # Generate invoice number if not provided (simple implementation)
    import random
    import string
    inv_num = invoice_in.reference_number or "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    new_invoice = Invoice(
        business_id=business.id,
        client_id=invoice_in.client_id,
        category_id=invoice_in.category_id,
        invoice_number=inv_num,
        invoice_date=invoice_in.invoice_date,
        due_date=invoice_in.due_date,
        payment_terms=invoice_in.payment_terms,
        notes=invoice_in.notes,
        payment_instructions=invoice_in.payment_instructions,
        footer_text=invoice_in.footer_text,
        currency=invoice_in.currency or business.currency or "USD",
        created_by=current_user.id
    )

    db.add(new_invoice)
    db.flush() # Get ID

    subtotal = 0.0
    for item_in in invoice_in.items:
        line_total = item_in.quantity * item_in.unit_price
        subtotal += line_total
        
        item = InvoiceItem(
            invoice_id=new_invoice.id,
            product_id=item_in.product_id,
            description=item_in.description,
            quantity=item_in.quantity,
            unit_price=item_in.unit_price,
            line_total=line_total,
            tax_rate=item_in.tax_rate,
            sort_order=item_in.sort_order
        )
        db.add(item)

    new_invoice.subtotal = subtotal
    new_invoice.total_amount = subtotal # Placeholder for actual tax/discount logic
    new_invoice.amount_due = new_invoice.total_amount

    db.commit()
    db.refresh(new_invoice)
    return new_invoice

@router.get("/", response_model=InvoiceListResponse)
def list_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None
):
    business = db.query(BusinessProfile).filter(BusinessProfile.user_id == current_user.id).first()
    if not business:
        return {"invoices": [], "total": 0, "page": 1, "page_size": limit, "total_pages": 0}

    query = db.query(Invoice).filter(Invoice.business_id == business.id)
    if status:
        query = query.filter(Invoice.status == status)
    
    total = query.count()
    invoices = query.offset(skip).limit(limit).all()
    
    return {
        "invoices": invoices,
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit
    }

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Check if user owns the business of this invoice
    business = db.query(BusinessProfile).filter(BusinessProfile.id == invoice.business_id).first()
    if not business or business.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this invoice")
        
    return invoice

@router.patch("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: str,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    business = db.query(BusinessProfile).filter(BusinessProfile.id == invoice.business_id).first()
    if not business or business.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this invoice")
        
    update_data = invoice_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(invoice, key, value)
        
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    business = db.query(BusinessProfile).filter(BusinessProfile.id == invoice.business_id).first()
    if not business or business.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this invoice")
        
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted successfully"}
