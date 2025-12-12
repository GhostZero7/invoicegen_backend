import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.business import BusinessProfile
from app.db.models.business import BusinessProfile as BusinessModel

@strawberry.type
class BusinessQuery:
    @strawberry.field
    async def my_businesses(self, info: strawberry.Info) -> List[BusinessProfile]:
        """Get all businesses owned by the current user"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        businesses = db.query(BusinessModel).filter(
            BusinessModel.user_id == user.id
        ).all()
        
        return [BusinessProfile(
            id=strawberry.ID(str(b.id)),
            user_id=strawberry.ID(str(b.user_id)),
            business_name=b.business_name,
            business_type=b.business_type,
            tax_id=b.tax_id,
            vat_number=b.vat_number,
            registration_number=b.registration_number,
            website=b.website,
            phone=b.phone,
            email=b.email,
            logo_url=b.logo_url,
            currency=b.currency,
            timezone=b.timezone,
            invoice_prefix=b.invoice_prefix,
            quote_prefix=b.quote_prefix,
            next_invoice_number=b.next_invoice_number,
            next_quote_number=b.next_quote_number,
            payment_terms_default=b.payment_terms_default,
            notes_default=b.notes_default,
            payment_instructions=b.payment_instructions,
            is_active=b.is_active,
            created_at=b.created_at,
            updated_at=b.updated_at
        ) for b in businesses]
    
    @strawberry.field
    async def business(self, info: strawberry.Info, id: strawberry.ID) -> Optional[BusinessProfile]:
        """Get a specific business by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        business = db.query(BusinessModel).filter(
            BusinessModel.id == str(id),
            BusinessModel.user_id == user.id
        ).first()
        
        if not business:
            return None
        
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
    
    @strawberry.field
    async def businesses(
        self, 
        info: strawberry.Info, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[BusinessProfile]:
        """Get all businesses (admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # For now, return user's businesses. Add admin check if needed
        businesses = db.query(BusinessModel).filter(
            BusinessModel.user_id == user.id
        ).offset(skip).limit(limit).all()
        
        return [BusinessProfile(
            id=strawberry.ID(str(b.id)),
            user_id=strawberry.ID(str(b.user_id)),
            business_name=b.business_name,
            business_type=b.business_type,
            tax_id=b.tax_id,
            vat_number=b.vat_number,
            registration_number=b.registration_number,
            website=b.website,
            phone=b.phone,
            email=b.email,
            logo_url=b.logo_url,
            currency=b.currency,
            timezone=b.timezone,
            invoice_prefix=b.invoice_prefix,
            quote_prefix=b.quote_prefix,
            next_invoice_number=b.next_invoice_number,
            next_quote_number=b.next_quote_number,
            payment_terms_default=b.payment_terms_default,
            notes_default=b.notes_default,
            payment_instructions=b.payment_instructions,
            is_active=b.is_active,
            created_at=b.created_at,
            updated_at=b.updated_at
        ) for b in businesses]
