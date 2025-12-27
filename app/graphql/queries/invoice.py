import strawberry
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.graphql.types.client import Client, ClientStatus, ClientType
from app.db.models.invoice import Invoice as InvoiceModel, InvoiceItem as InvoiceItemModel
from app.db.models.business import BusinessProfile
from app.db.models.client import Client as ClientModel
from redis import asyncio as aioredis
import json
import logging
from datetime import date, datetime
import json

logger = logging.getLogger(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError ("Type %s not serializable" % type(obj))



def parse_iso_dates(data_list: list) -> list:
    """Helper to convert ISO 8601 strings back into date/datetime objects."""
    parsed_list = []
    # Define the fields that are dates/datetimes in your Invoice model
    date_fields = [
        'invoice_date', 'due_date', 'sent_at', 'viewed_at', 
        'paid_at', 'cancelled_at', 'created_at', 'updated_at'
    ]

    for item in data_list:
        parsed_item = item.copy()
        
        for field in date_fields:
            value = parsed_item.get(field)
            if value and isinstance(value, str):
                try:
                    # Check if it contains time information (datetime) or just date
                    if 'T' in value:
                        parsed_item[field] = datetime.fromisoformat(value)
                    else:
                        parsed_item[field] = date.fromisoformat(value)
                except ValueError:
                    # Handle potential bad data gracefully
                    print(f"Could not parse ISO date for field {field}: {value}")
                    parsed_item[field] = None # Set to None if parsing fails
        
        # Recursively parse dates in the nested client dictionary if it exists
        if "client" in parsed_item and isinstance(parsed_item["client"], dict):
            client_data = parsed_item["client"]
            for field in ['created_at', 'updated_at']:
                val = client_data.get(field)
                if val and isinstance(val, str):
                    try:
                        if 'T' in val:
                            client_data[field] = datetime.fromisoformat(val)
                        else:
                            client_data[field] = date.fromisoformat(val)
                    except ValueError:
                        pass
            parsed_item["client"] = client_data

        parsed_list.append(parsed_item)
    return parsed_list

@strawberry.type
class InvoiceQuery:
    @strawberry.field
    async def invoice(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Invoice]:
        """Get a specific invoice by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        invoice = db.query(InvoiceModel).join(BusinessProfile).filter(
            InvoiceModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not invoice:
            return None
        
        # query client
        client = db.query(ClientModel).filter(ClientModel.id == str(invoice.client_id)).first()
        if not client:
            return Exception('Client not found')

        
        return Invoice(
            id=strawberry.ID(str(invoice.id)),
            business_id=strawberry.ID(str(invoice.business_id)),
            client_id=strawberry.ID(str(invoice.client_id)),
            client=Client(
                id=strawberry.ID(str(client.id)),
                business_id=strawberry.ID(str(client.business_id)),
                first_name=client.first_name,
                last_name=client.last_name,
                status=client.status,
                phone=client.phone,
                email=client.email,
                notes=client.notes,
                company_name=client.company_name,
                created_at=client.created_at,
                updated_at=client.updated_at,
                client_type=client.client_type,
                mobile=client.mobile,
                website=client.website,
                tax_id=client.tax_id,
                vat_number=client.vat_number,
                payment_terms=client.payment_terms,
                credit_limit=client.credit_limit,
                currency=client.currency,
                language=client.language 
            ),
            invoice_number=invoice.invoice_number,
            reference_number=invoice.reference_number,
            purchase_order_number=invoice.purchase_order_number,
            status=invoice.status,
            invoice_date=invoice.invoice_date,
            due_date=invoice.due_date,
            payment_terms=invoice.payment_terms.value,
            subtotal=invoice.subtotal,
            discount_type=invoice.discount_type,
            discount_value=invoice.discount_value,
            discount_amount=invoice.discount_amount,
            tax_amount=invoice.tax_amount,
            shipping_amount=invoice.shipping_amount,
            total_amount=invoice.total_amount,
            amount_paid=invoice.amount_paid,
            amount_due=invoice.amount_due,
            currency=invoice.currency,
            notes=invoice.notes,
            payment_instructions=invoice.payment_instructions,
            footer_text=invoice.footer_text,
            is_recurring=invoice.is_recurring,
            sent_at=invoice.sent_at,
            viewed_at=invoice.viewed_at,
            paid_at=invoice.paid_at,
            cancelled_at=invoice.cancelled_at,
            created_at=invoice.created_at,
            updated_at=invoice.updated_at
        )
    
    @strawberry.field
    async def invoices(
        self,
        info: strawberry.Info,
        business_id: Optional[strawberry.ID] = None,
        client_id: Optional[strawberry.ID] = None,
        status: Optional[InvoiceStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Invoice]:
        """Get invoices with optional filters"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        redis_client: aioredis.Redis = info.context["redis"]

        if not user:
            raise Exception("Not authenticated")


        
        cache_key_params = f"{business_id=}:{client_id=}:{status=}:{skip=}:{limit=}"
        cache_key = f"user:{user.id}:invoices:{cache_key_params}"

        cached_data = await redis_client.getex(cache_key)
        if cached_data:
            print("💾 Returning invoices from cache")
            # 1. Deserialize the JSON string back into a list of dictionaries
            data_list_raw = json.loads(cached_data)
            # 2. Parse the string dates back into date objects
            data_list_parsed = parse_iso_dates(data_list_raw)            
            # 3. Convert dictionaries back into the Strawberry Type instances
            invoices = []
            for data in data_list_parsed:
                if data.get("client") and isinstance(data["client"], dict):
                    data["client"] = Client(**data["client"])
                invoices.append(Invoice(**data))
            return invoices

        
        query = db.query(InvoiceModel).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id
        )
        
        if business_id:
            query = query.filter(InvoiceModel.business_id == str(business_id))
        
        if client_id:
            query = query.filter(InvoiceModel.client_id == str(client_id))
        
        if status:
            query = query.filter(InvoiceModel.status == status.value)
        
        invoices = query.order_by(InvoiceModel.created_at.desc()).offset(skip).limit(limit).all()

        # Optimize client fetching to avoid N+1 problem
        client_ids = {str(inv.client_id) for inv in invoices if inv.client_id}
        clients = db.query(ClientModel).filter(ClientModel.id.in_(client_ids)).all() if client_ids else []
        clients_map = {str(c.id): c for c in clients}

        def get_client_from_map(client_id_val):
            if not client_id_val or str(client_id_val) not in clients_map:
                return None
            
            client = clients_map[str(client_id_val)]
            
            return Client(
                id=strawberry.ID(str(client.id)),
                business_id=strawberry.ID(str(client.business_id)),
                first_name=client.first_name,
                last_name=client.last_name,
                status=client.status,
                phone=client.phone,
                email=client.email,
                notes=client.notes,
                company_name=client.company_name,
                created_at=client.created_at,
                updated_at=client.updated_at,
                client_type=client.client_type,
                mobile=client.mobile,
                website=client.website,
                tax_id=client.tax_id,
                vat_number=client.vat_number,
                payment_terms=client.payment_terms,
                credit_limit=client.credit_limit,
                currency=client.currency,
                language=client.language 
            )
        
        invoices_typed_list = [Invoice(
            id=strawberry.ID(str(inv.id)),
            business_id=strawberry.ID(str(inv.business_id)),
            client_id=strawberry.ID(str(inv.client_id)),
            invoice_number=inv.invoice_number,
            client=get_client_from_map(inv.client_id),
            reference_number=inv.reference_number,
            purchase_order_number=inv.purchase_order_number,
            status=inv.status,
            invoice_date=inv.invoice_date,
            due_date=inv.due_date,
            payment_terms=inv.payment_terms.value,
            subtotal=inv.subtotal,
            discount_type=inv.discount_type,
            discount_value=inv.discount_value,
            discount_amount=inv.discount_amount,
            tax_amount=inv.tax_amount,
            shipping_amount=inv.shipping_amount,
            total_amount=inv.total_amount,
            amount_paid=inv.amount_paid,
            amount_due=inv.amount_due,
            currency=inv.currency,
            notes=inv.notes,
            payment_instructions=inv.payment_instructions,
            footer_text=inv.footer_text,
            is_recurring=inv.is_recurring,
            sent_at=inv.sent_at,
            viewed_at=inv.viewed_at,
            paid_at=inv.paid_at,
            cancelled_at=inv.cancelled_at,
            created_at=inv.created_at,
            updated_at=inv.updated_at
        ) for inv in invoices]

        json_data = json.dumps(
        [inv.__dict__ for inv in invoices_typed_list], 
        default=json_serial # <-- FIX APPLIED HERE
    )
        await redis_client.setex(cache_key, 300, json_data)
        print(f"Storing result in cache key: {cache_key} with 300s TTL")

        return invoices_typed_list
    
    @strawberry.field
    async def invoice_items(self, info: strawberry.Info, invoice_id: strawberry.ID) -> List[InvoiceItem]:
        """Get all items for a specific invoice"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business that owns this invoice
        items = db.query(InvoiceItemModel).join(
            InvoiceModel, InvoiceItemModel.invoice_id == InvoiceModel.id
        ).join(BusinessProfile).filter(
            InvoiceItemModel.invoice_id == str(invoice_id),
            BusinessProfile.user_id == user.id
        ).order_by(InvoiceItemModel.sort_order).all()
        
        return [InvoiceItem(
            id=strawberry.ID(str(item.id)),
            invoice_id=strawberry.ID(str(item.invoice_id)),
            product_id=strawberry.ID(str(item.product_id)) if item.product_id else None,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            unit_of_measure=item.unit_of_measure,
            tax_rate=item.tax_rate,
            tax_amount=item.tax_amount,
            discount_type=item.discount_type,
            discount_value=item.discount_value,
            discount_amount=item.discount_amount,
            line_total=item.line_total,
            sort_order=item.sort_order
        ) for item in items]
