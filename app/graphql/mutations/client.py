import strawberry
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.graphql.types.client import Client, CreateClientInput, UpdateClientInput
from app.db.models.client import Client as ClientModel
from app.db.models.business import BusinessProfile

@strawberry.type
class ClientMutation:
    @strawberry.mutation
    async def create_client(self, info: strawberry.Info, input: CreateClientInput) -> Client:
        """Create a new client"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business
        business = db.query(BusinessProfile).filter(
            BusinessProfile.id == str(input.business_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        client = ClientModel(
            id=str(uuid.uuid4()),
            business_id=str(input.business_id),
            client_type=input.client_type.value,
            company_name=input.company_name,
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            phone=input.phone,
            mobile=input.mobile,
            website=input.website,
            tax_id=input.tax_id,
            payment_terms=input.payment_terms,
            currency=input.currency or "USD",
            language="en",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        return Client(
            id=strawberry.ID(str(client.id)),
            business_id=strawberry.ID(str(client.business_id)),
            client_type=client.client_type,
            company_name=client.company_name,
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email,
            phone=client.phone,
            mobile=client.mobile,
            website=client.website,
            tax_id=client.tax_id,
            vat_number=client.vat_number,
            payment_terms=client.payment_terms,
            credit_limit=client.credit_limit,
            currency=client.currency,
            language=client.language,
            notes=client.notes,
            status=client.status,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
    
    @strawberry.mutation
    async def update_client(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdateClientInput
    ) -> Client:
        """Update an existing client"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        client = db.query(ClientModel).join(BusinessProfile).filter(
            ClientModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not client:
            raise Exception("Client not found")
        
        if input.company_name is not None:
            client.company_name = input.company_name
        if input.first_name is not None:
            client.first_name = input.first_name
        if input.last_name is not None:
            client.last_name = input.last_name
        if input.email is not None:
            client.email = input.email
        if input.phone is not None:
            client.phone = input.phone
        if input.mobile is not None:
            client.mobile = input.mobile
        if input.website is not None:
            client.website = input.website
        if input.tax_id is not None:
            client.tax_id = input.tax_id
        if input.vat_number is not None:
            client.vat_number = input.vat_number
        if input.payment_terms is not None:
            client.payment_terms = input.payment_terms
        if input.credit_limit is not None:
            client.credit_limit = input.credit_limit
        if input.notes is not None:
            client.notes = input.notes
        if input.status is not None:
            client.status = input.status.value
        
        client.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(client)
        
        return Client(
            id=strawberry.ID(str(client.id)),
            business_id=strawberry.ID(str(client.business_id)),
            client_type=client.client_type,
            company_name=client.company_name,
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email,
            phone=client.phone,
            mobile=client.mobile,
            website=client.website,
            tax_id=client.tax_id,
            vat_number=client.vat_number,
            payment_terms=client.payment_terms,
            credit_limit=client.credit_limit,
            currency=client.currency,
            language=client.language,
            notes=client.notes,
            status=client.status,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
    
    @strawberry.mutation
    async def delete_client(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a client"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        client = db.query(ClientModel).join(BusinessProfile).filter(
            ClientModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not client:
            raise Exception("Client not found")
        
        db.delete(client)
        db.commit()
        
        return True
