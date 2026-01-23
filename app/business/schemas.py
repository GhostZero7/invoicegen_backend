from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.db.models.business import BusinessType, PaymentTerms

class BusinessProfileBase(BaseModel):
    business_name: str
    business_type: BusinessType
    tax_id: Optional[str] = None
    vat_number: Optional[str] = None
    registration_number: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr
    logo_url: Optional[str] = None
    currency: str = "USD"
    timezone: str = "UTC"
    fiscal_year_end: Optional[date] = None
    invoice_prefix: str = "INV"
    quote_prefix: str = "QUO"
    next_invoice_number: int = 1
    next_quote_number: int = 1
    payment_terms_default: PaymentTerms = PaymentTerms.NET_30
    notes_default: Optional[str] = None
    payment_instructions: Optional[str] = None
    is_active: bool = True
    is_premium: bool = False

class BusinessProfileCreate(BusinessProfileBase):
    pass

class BusinessProfileUpdate(BaseModel):
    business_name: Optional[str] = None
    business_type: Optional[BusinessType] = None
    tax_id: Optional[str] = None
    vat_number: Optional[str] = None
    registration_number: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    logo_url: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    fiscal_year_end: Optional[date] = None
    invoice_prefix: Optional[str] = None
    quote_prefix: Optional[str] = None
    next_invoice_number: Optional[int] = None
    next_quote_number: Optional[int] = None
    payment_terms_default: Optional[PaymentTerms] = None
    notes_default: Optional[str] = None
    payment_instructions: Optional[str] = None
    is_active: Optional[bool] = None
    is_premium: Optional[bool] = None

class BusinessProfileResponse(BusinessProfileBase):
    id: str
    user_id: str
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True