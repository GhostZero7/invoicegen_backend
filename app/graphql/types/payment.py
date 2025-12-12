import strawberry
from datetime import date, datetime
from typing import Optional
from enum import Enum

@strawberry.enum
class PaymentMethod(Enum):
    CASH = "cash"
    CHECK = "check"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    OTHER = "other"

@strawberry.enum
class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@strawberry.type
class Payment:
    id: strawberry.ID
    invoice_id: strawberry.ID
    payment_number: str
    payment_date: date
    amount: float
    payment_method: PaymentMethod
    transaction_id: Optional[str]
    reference_number: Optional[str]
    notes: Optional[str]
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

@strawberry.input
class CreatePaymentInput:
    invoice_id: strawberry.ID
    payment_date: date
    amount: float
    payment_method: PaymentMethod
    transaction_id: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None

@strawberry.input
class UpdatePaymentInput:
    payment_date: Optional[date] = None
    amount: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    transaction_id: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[PaymentStatus] = None
