# GraphQL Implementation Guide

## Current Status

✅ **Completed:**
- User model (queries, mutations, types)
- GraphQL schemas for: Invoice, Business, Client, Payment
- Strawberry types for: Business, Client

🔄 **In Progress:**
- Invoice, Payment types
- Query resolvers for all models
- Mutation resolvers for all models

## Database Schema Issue

**Error:** `column "category_id" of relation "invoices" does not exist`

**Solution:** Run database migrations or create tables:

```bash
# Option 1: Run migrations
alembic upgrade head

# Option 2: Create tables directly
python create_tables.py
```

## Remaining Implementation Steps

### 1. Complete Strawberry Types

Create these files:

**`app/graphql/types/invoice.py`**
```python
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
    line_total: float

@strawberry.input
class InvoiceItemInput:
    product_id: Optional[strawberry.ID] = None
    description: str
    quantity: float
    unit_price: float
    unit_of_measure: Optional[str] = "unit"
    tax_rate: Optional[float] = 0.0

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

@strawberry.input
class UpdateInvoiceInput:
    status: Optional[InvoiceStatus] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None
```

**`app/graphql/types/payment.py`**
```python
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
```

### 2. Create Query Resolvers

**`app/graphql/queries/business.py`**
```python
import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.business import BusinessProfile
from app.db.models.business import BusinessProfile as BusinessModel

def business_model_to_type(business: BusinessModel) -> BusinessProfile:
    from app.graphql.types.business import BusinessType, PaymentTerms
    return BusinessProfile(
        id=strawberry.ID(business.id),
        user_id=strawberry.ID(business.user_id),
        business_name=business.business_name,
        business_type=BusinessType(business.business_type.value),
        tax_id=business.tax_id,
        vat_number=business.vat_number,
        registration_number=business.registration_number,
        website=business.website,
        phone=business.phone,
        email=business.email,
        logo_url=business.logo_url,
        currency=business.currency,
        timezone=business.timezone,
        invoice_prefix=business.invoice_prefix,
        quote_prefix=business.quote_prefix,
        next_invoice_number=business.next_invoice_number,
        next_quote_number=business.next_quote_number,
        payment_terms_default=PaymentTerms(business.payment_terms_default.value),
        notes_default=business.notes_default,
        payment_instructions=business.payment_instructions,
        is_active=business.is_active,
        created_at=business.created_at,
        updated_at=business.updated_at,
    )

@strawberry.type
class BusinessQuery:
    @strawberry.field
    def my_businesses(self, info: strawberry.Info) -> List[BusinessProfile]:
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            raise Exception("Not authenticated")
        
        businesses = db.query(BusinessModel).filter(
            BusinessModel.user_id == current_user.id
        ).all()
        
        return [business_model_to_type(b) for b in businesses]
    
    @strawberry.field
    def business(self, info: strawberry.Info, id: strawberry.ID) -> Optional[BusinessProfile]:
        db: Session = info.context["db"]
        business = db.query(BusinessModel).filter(BusinessModel.id == str(id)).first()
        
        if not business:
            return None
        
        return business_model_to_type(business)
    
    @strawberry.field
    def businesses(
        self,
        info: strawberry.Info,
        skip: int = 0,
        limit: int = 10
    ) -> List[BusinessProfile]:
        db: Session = info.context["db"]
        businesses = db.query(BusinessModel).offset(skip).limit(limit).all()
        
        return [business_model_to_type(b) for b in businesses]
```

Follow the same pattern for:
- `app/graphql/queries/client.py`
- `app/graphql/queries/invoice.py`
- `app/graphql/queries/payment.py`

### 3. Create Mutation Resolvers

**`app/graphql/mutations/business.py`**
```python
import strawberry
import uuid
from sqlalchemy.orm import Session
from app.graphql.types.business import (
    BusinessProfile,
    CreateBusinessInput,
    UpdateBusinessInput,
)
from app.db.models.business import BusinessProfile as BusinessModel
from app.graphql.queries.business import business_model_to_type

@strawberry.type
class BusinessMutation:
    @strawberry.mutation
    def create_business(
        self,
        info: strawberry.Info,
        input: CreateBusinessInput
    ) -> BusinessProfile:
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            raise Exception("Not authenticated")
        
        business = BusinessModel(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            business_name=input.business_name,
            business_type=input.business_type.value,
            tax_id=input.tax_id,
            email=input.email,
            phone=input.phone,
            currency=input.currency or "USD",
            invoice_prefix=input.invoice_prefix or "INV",
        )
        
        db.add(business)
        db.commit()
        db.refresh(business)
        
        return business_model_to_type(business)
    
    @strawberry.mutation
    def update_business(
        self,
        info: strawberry.Info,
        id: strawberry.ID,
        input: UpdateBusinessInput
    ) -> BusinessProfile:
        db: Session = info.context["db"]
        
        business = db.query(BusinessModel).filter(BusinessModel.id == str(id)).first()
        if not business:
            raise Exception("Business not found")
        
        # Update fields
        if input.business_name is not None:
            business.business_name = input.business_name
        if input.email is not None:
            business.email = input.email
        # ... update other fields
        
        db.commit()
        db.refresh(business)
        
        return business_model_to_type(business)
    
    @strawberry.mutation
    def delete_business(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        db: Session = info.context["db"]
        
        business = db.query(BusinessModel).filter(BusinessModel.id == str(id)).first()
        if not business:
            raise Exception("Business not found")
        
        business.is_active = False
        db.commit()
        
        return True
```

Follow the same pattern for:
- `app/graphql/mutations/client.py`
- `app/graphql/mutations/invoice.py`
- `app/graphql/mutations/payment.py`

### 4. Update Schema

**`app/graphql/schema.py`**
```python
import strawberry
from app.graphql.queries.user import UserQuery
from app.graphql.queries.business import BusinessQuery
from app.graphql.queries.client import ClientQuery
from app.graphql.queries.invoice import InvoiceQuery
from app.graphql.queries.payment import PaymentQuery

from app.graphql.mutations.user import UserMutation
from app.graphql.mutations.business import BusinessMutation
from app.graphql.mutations.client import ClientMutation
from app.graphql.mutations.invoice import InvoiceMutation
from app.graphql.mutations.payment import PaymentMutation

@strawberry.type
class Query(
    UserQuery,
    BusinessQuery,
    ClientQuery,
    InvoiceQuery,
    PaymentQuery
):
    """Root Query combining all query types"""
    pass

@strawberry.type
class Mutation(
    UserMutation,
    BusinessMutation,
    ClientMutation,
    InvoiceMutation,
    PaymentMutation
):
    """Root Mutation combining all mutation types"""
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### 5. Update __init__ Files

**`app/graphql/types/__init__.py`**
```python
from .user import *
from .business import *
from .client import *
from .invoice import *
from .payment import *
```

**`app/graphql/queries/__init__.py`**
```python
from .user import UserQuery
from .business import BusinessQuery
from .client import ClientQuery
from .invoice import InvoiceQuery
from .payment import PaymentQuery

__all__ = [
    "UserQuery",
    "BusinessQuery",
    "ClientQuery",
    "InvoiceQuery",
    "PaymentQuery",
]
```

**`app/graphql/mutations/__init__.py`**
```python
from .user import UserMutation
from .business import BusinessMutation
from .client import ClientMutation
from .invoice import InvoiceMutation
from .payment import PaymentMutation

__all__ = [
    "UserMutation",
    "BusinessMutation",
    "ClientMutation",
    "InvoiceMutation",
    "PaymentMutation",
]
```

## Testing

After implementation, test with these queries:

### Business
```graphql
query {
  myBusinesses {
    id
    businessName
    email
  }
}

mutation {
  createBusiness(input: {
    businessName: "My Company"
    businessType: LLC
    email: "company@example.com"
  }) {
    id
    businessName
  }
}
```

### Client
```graphql
query {
  clients(businessId: "business-id") {
    id
    email
    companyName
  }
}

mutation {
  createClient(input: {
    businessId: "business-id"
    clientType: COMPANY
    companyName: "Client Corp"
    email: "client@example.com"
  }) {
    id
    companyName
  }
}
```

### Invoice
```graphql
query {
  invoices(businessId: "business-id", status: PAID) {
    id
    invoiceNumber
    totalAmount
    status
  }
}

mutation {
  createInvoice(input: {
    businessId: "business-id"
    clientId: "client-id"
    invoiceDate: "2024-01-01"
    dueDate: "2024-01-31"
    paymentTerms: "net_30"
    items: [{
      description: "Service"
      quantity: 1
      unitPrice: 100.00
    }]
  }) {
    id
    invoiceNumber
    totalAmount
  }
}
```

## Priority Order

1. Fix database schema (run migrations)
2. Complete Invoice types and resolvers (most important)
3. Complete Client types and resolvers
4. Complete Business types and resolvers
5. Complete Payment types and resolvers

## Notes

- All converters follow the pattern: `model_to_type()`
- All mutations require authentication check
- Use `info.context["db"]` for database session
- Use `info.context.get("current_user")` for current user
- Always commit and refresh after database changes
