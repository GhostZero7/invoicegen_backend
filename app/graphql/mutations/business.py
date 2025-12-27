import strawberry
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.graphql.types.business import BusinessProfile, CreateBusinessInput, UpdateBusinessInput
from app.db.models.business import BusinessProfile as BusinessModel
from app.services.billing_service import BillingService

@strawberry.type
class BusinessMutation:
    @strawberry.mutation
    async def create_business(self, info: strawberry.Info, input: CreateBusinessInput) -> BusinessProfile:
        """Create a new business profile"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
            
        # Check billing limits
        if not BillingService.can_create_business(db, user.id):
            raise Exception("Maximum business profiles reached for your plan. Please upgrade to create more.")
        
        business = BusinessModel(
            id=str(uuid.uuid4()),
            user_id=user.id,
            business_name=input.business_name,
            business_type=input.business_type.value,
            tax_id=input.tax_id,
            email=input.email,
            phone=input.phone,
            currency=input.currency or "USD",
            invoice_prefix=input.invoice_prefix or "INV",
            timezone="UTC",
            quote_prefix="QUO",
            next_invoice_number=1,
            next_quote_number=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(business)
        db.commit()
        db.refresh(business)
        
        return BusinessProfile(
            id=strawberry.ID(str(business.id)),
            user_id=strawberry.ID(str(business.user_id)),
            business_name=business.business_name,
            business_type=business.business_type,
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
            payment_terms_default=business.payment_terms_default,
            notes_default=business.notes_default,
            payment_instructions=business.payment_instructions,
            is_active=business.is_active,
            created_at=business.created_at,
            updated_at=business.updated_at
        )
    
    @strawberry.mutation
    async def update_business(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdateBusinessInput
    ) -> BusinessProfile:
        """Update an existing business profile"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        business = db.query(BusinessModel).filter(
            BusinessModel.id == str(id),
            BusinessModel.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        if input.business_name is not None:
            business.business_name = input.business_name
        if input.business_type is not None:
            business.business_type = input.business_type.value
        if input.tax_id is not None:
            business.tax_id = input.tax_id
        if input.vat_number is not None:
            business.vat_number = input.vat_number
        if input.website is not None:
            business.website = input.website
        if input.phone is not None:
            business.phone = input.phone
        if input.email is not None:
            business.email = input.email
        if input.logo_url is not None:
            business.logo_url = input.logo_url
        if input.currency is not None:
            business.currency = input.currency
        if input.timezone is not None:
            business.timezone = input.timezone
        if input.payment_terms_default is not None:
            business.payment_terms_default = input.payment_terms_default.value
        if input.notes_default is not None:
            business.notes_default = input.notes_default
        if input.payment_instructions is not None:
            business.payment_instructions = input.payment_instructions
        if input.is_active is not None:
            business.is_active = input.is_active
        
        business.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(business)
        
        return BusinessProfile(
            id=strawberry.ID(str(business.id)),
            user_id=strawberry.ID(str(business.user_id)),
            business_name=business.business_name,
            business_type=business.business_type,
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
            payment_terms_default=business.payment_terms_default,
            notes_default=business.notes_default,
            payment_instructions=business.payment_instructions,
            is_active=business.is_active,
            created_at=business.created_at,
            updated_at=business.updated_at
        )
    
    @strawberry.mutation
    async def delete_business(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a business profile"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        business = db.query(BusinessModel).filter(
            BusinessModel.id == str(id),
            BusinessModel.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        db.delete(business)
        db.commit()
        
        return True
