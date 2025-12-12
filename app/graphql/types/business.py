import strawberry
from datetime import date
from typing import Optional
from enum import Enum

@strawberry.enum
class BusinessType(Enum):
    SOLE_PROPRIETOR = "sole_proprietor"
    LLC = "llc"
    CORPORATION = "corporation"
    PARTNERSHIP = "partnership"

@strawberry.enum
class PaymentTerms(Enum):
    DUE_ON_RECEIPT = "due_on_receipt"
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_60 = "net_60"
    CUSTOM = "custom"

@strawberry.type
class BusinessProfile:
    id: strawberry.ID
    user_id: strawberry.ID
    business_name: str
    business_type: BusinessType
    tax_id: Optional[str]
    vat_number: Optional[str]
    registration_number: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    email: str
    logo_url: Optional[str]
    currency: str
    timezone: str
    invoice_prefix: str
    quote_prefix: str
    next_invoice_number: int
    next_quote_number: int
    payment_terms_default: PaymentTerms
    notes_default: Optional[str]
    payment_instructions: Optional[str]
    is_active: bool
    created_at: date
    updated_at: date

@strawberry.input
class CreateBusinessInput:
    business_name: str
    business_type: BusinessType
    email: str
    tax_id: Optional[str] = None
    phone: Optional[str] = None
    currency: Optional[str] = "USD"
    invoice_prefix: Optional[str] = "INV"

@strawberry.input
class UpdateBusinessInput:
    business_name: Optional[str] = None
    business_type: Optional[BusinessType] = None
    tax_id: Optional[str] = None
    vat_number: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_url: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    payment_terms_default: Optional[PaymentTerms] = None
    notes_default: Optional[str] = None
    payment_instructions: Optional[str] = None
    is_active: Optional[bool] = None
