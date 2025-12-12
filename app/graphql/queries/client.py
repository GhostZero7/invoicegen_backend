import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.client import Client, ClientType, ClientStatus
from app.db.models.client import Client as ClientModel
from app.db.models.business import BusinessProfile

@strawberry.type
class ClientQuery:
    @strawberry.field
    async def client(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Client]:
        """Get a specific client by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business that owns this client
        client = db.query(ClientModel).join(BusinessProfile).filter(
            ClientModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not client:
            return None
        
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
    
    @strawberry.field
    async def clients(
        self,
        info: strawberry.Info,
        business_id: Optional[strawberry.ID] = None,
        skip: int = 0,
        limit: int = 10,
        status: Optional[ClientStatus] = None,
        client_type: Optional[ClientType] = None
    ) -> List[Client]:
        """Get clients with optional filters"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        query = db.query(ClientModel).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id
        )
        
        if business_id:
            query = query.filter(ClientModel.business_id == str(business_id))
        
        if status:
            query = query.filter(ClientModel.status == status.value)
        
        if client_type:
            query = query.filter(ClientModel.client_type == client_type.value)
        
        clients = query.offset(skip).limit(limit).all()
        
        return [Client(
            id=strawberry.ID(str(c.id)),
            business_id=strawberry.ID(str(c.business_id)),
            client_type=c.client_type,
            company_name=c.company_name,
            first_name=c.first_name,
            last_name=c.last_name,
            email=c.email,
            phone=c.phone,
            mobile=c.mobile,
            website=c.website,
            tax_id=c.tax_id,
            vat_number=c.vat_number,
            payment_terms=c.payment_terms,
            credit_limit=c.credit_limit,
            currency=c.currency,
            language=c.language,
            notes=c.notes,
            status=c.status,
            created_at=c.created_at,
            updated_at=c.updated_at
        ) for c in clients]
