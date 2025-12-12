import strawberry
from datetime import date
from typing import Optional
from enum import Enum

@strawberry.enum
class ClientType(Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

@strawberry.enum
class ClientStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

@strawberry.type
class Client:
    id: strawberry.ID
    business_id: strawberry.ID
    client_type: ClientType
    company_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    phone: Optional[str]
    mobile: Optional[str]
    website: Optional[str]
    tax_id: Optional[str]
    vat_number: Optional[str]
    payment_terms: Optional[str]
    credit_limit: Optional[float]
    currency: str
    language: str
    notes: Optional[str]
    status: ClientStatus
    created_at: date
    updated_at: date

@strawberry.input
class CreateClientInput:
    business_id: strawberry.ID
    client_type: ClientType
    email: str
    company_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    tax_id: Optional[str] = None
    payment_terms: Optional[str] = None
    currency: Optional[str] = "USD"

@strawberry.input
class UpdateClientInput:
    company_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    tax_id: Optional[str] = None
    vat_number: Optional[str] = None
    payment_terms: Optional[str] = None
    credit_limit: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[ClientStatus] = None
