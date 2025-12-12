import strawberry
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

@strawberry.enum
class InvoiceStatus(Enum):
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@strawberry.enum
class DiscountType(Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

@strawberry.type
class Invoice:
    id: strawberry.ID
    business_id: strawberry.ID
    client_id: strawberry.ID
    invoice_number: str
    reference_number: Optional[str]
    purchase_order_number: Optional[str]
    status: InvoiceStatus
    invoice_date: date
    due_date: date
    payment_terms: str
    subtotal: float
    discount_type: Optional[DiscountType]
    discount_value: float
    discount_amount: float
    tax_amount: float
    shipping_amount: float
    total_amount: float
    amount_paid: float
    amount_due: float
    currency: str
    notes: Optional[str]
    payment_instructions: Optional[str]
    footer_text: Optional[str]
    is_recurring: bool
    sent_at: Optional[datetime]
    viewed_at: Optional[datetime]
    paid_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

@strawberry.type
class InvoiceItem:
    id: strawberry.ID
    invoice_id: strawberry.ID
    product_id: Optional[strawberry.ID]
    description: str
    quantity: float
    unit_price: float
    unit_of_measure: str
    tax_rate: float
    tax_amount: float
    discount_type: Optional[DiscountType]
    discount_value: float
    discount_amount: float
    line_total: float
    sort_order: int

@strawberry.input
class InvoiceItemInput:
    product_id: Optional[strawberry.ID] = None
    description: str = ""
    quantity: float = 1.0
    unit_price: float = 0.0
    unit_of_measure: Optional[str] = "unit"
    tax_rate: Optional[float] = 0.0
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = 0.0

@strawberry.input
class CreateInvoiceInput:
    business_id: strawberry.ID
    client_id: strawberry.ID
    invoice_date: date
    due_date: date
    payment_terms: str
    items: List[InvoiceItemInput]
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = 0.0
    shipping_amount: Optional[float] = 0.0
    notes: Optional[str] = None
    payment_instructions: Optional[str] = None

@strawberry.input
class UpdateInvoiceInput:
    status: Optional[InvoiceStatus] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None
    payment_instructions: Optional[str] = None
