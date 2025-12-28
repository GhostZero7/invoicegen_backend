from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class ClientType(str, Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

class ClientStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

class ClientBase(BaseModel):
    client_type: ClientType = ClientType.INDIVIDUAL
    company_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    tax_id: Optional[str] = None
    vat_number: Optional[str] = None
    payment_terms: Optional[str] = None
    currency: str = "USD"
    language: str = "en"
    notes: Optional[str] = None
    status: ClientStatus = ClientStatus.ACTIVE

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    client_type: Optional[ClientType] = None
    company_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[ClientStatus] = None

class ClientResponse(ClientBase):
    id: str
    business_id: str
    client_name: str
    created_at: date
    updated_at: date

    @validator('client_name', pre=True, always=True)
    def set_client_name(cls, v, values):
        if v: return v
        company = values.get('company_name')
        first = values.get('first_name')
        last = values.get('last_name')
        if company:
            return company
        if first and last:
            return f"{first} {last}"
        return first or last or "Unknown Client"

    class Config:
        from_attributes = True
