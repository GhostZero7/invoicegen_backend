from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum
from decimal import Decimal

# Enums
class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentTerms(str, Enum):
    DUE_ON_RECEIPT = "due_on_receipt"
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_60 = "net_60"
    CUSTOM = "custom"

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

# Invoice Item Schemas
class InvoiceItemBase(BaseModel):
    product_id: Optional[str] = None
    description: str
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    unit_of_measure: str = "unit"
    tax_rate: float = Field(ge=0, le=100, default=0.0)
    discount_type: Optional[DiscountType] = None
    discount_value: float = Field(ge=0, default=0.0)
    sort_order: int = 0

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemUpdate(InvoiceItemBase):
    pass

class InvoiceItemResponse(InvoiceItemBase):
    id: str
    invoice_id: str
    tax_amount: float
    discount_amount: float
    line_total: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

# Invoice Schemas
class InvoiceBase(BaseModel):
    client_id: str
    category_id: Optional[str] = None
    invoice_date: date = Field(default_factory=date.today)
    due_date: date
    payment_terms: PaymentTerms = PaymentTerms.NET_30
    custom_due_days: Optional[int] = None
    discount_type: Optional[DiscountType] = None
    discount_value: float = Field(ge=0, default=0.0)
    tax_amount: float = Field(ge=0, default=0.0)
    shipping_amount: float = Field(ge=0, default=0.0)
    notes: Optional[str] = None
    payment_instructions: Optional[str] = None
    footer_text: Optional[str] = None
    reference_number: Optional[str] = None
    purchase_order_number: Optional[str] = None
    
    @validator('due_date')
    def due_date_after_invoice_date(cls, v, values):
        if 'invoice_date' in values and v < values['invoice_date']:
            raise ValueError('Due date must be on or after invoice date')
        return v

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None
    recurring_end_date: Optional[date] = None

class InvoiceUpdate(BaseModel):
    client_id: Optional[str] = None
    category_id: Optional[str] = None
    status: Optional[InvoiceStatus] = None
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    payment_terms: Optional[PaymentTerms] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = None
    tax_amount: Optional[float] = None
    shipping_amount: Optional[float] = None
    notes: Optional[str] = None
    payment_instructions: Optional[str] = None
    footer_text: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    id: str
    business_id: str
    invoice_number: str
    status: InvoiceStatus
    subtotal: float
    discount_amount: float
    total_amount: float
    amount_paid: float
    amount_due: float
    currency: str = "USD"
    exchange_rate: float = 1.0000
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None
    recurring_end_date: Optional[date] = None
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    pdf_url: Optional[str] = None
    public_url: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItemResponse] = []
    
    class Config:
        orm_mode = True
        from_attributes = True

# Invoice List Response
class InvoiceListResponse(BaseModel):
    invoices: List[InvoiceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# Invoice Summary
class InvoiceSummary(BaseModel):
    total_invoices: int
    total_revenue: float
    outstanding_balance: float
    paid_invoices: int
    overdue_invoices: int
    average_invoice_amount: float