import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.graphql.types.product import Product, ProductFilterInput
from app.db.models.product import Product as ProductModel
from app.db.models.business import BusinessProfile

def product_model_to_type(product_model: ProductModel) -> Product:
    """Convert SQLAlchemy Product model to Strawberry Product type"""
    return Product(
        id=strawberry.ID(product_model.id),
        business_id=strawberry.ID(product_model.business_id),
        sku=product_model.sku,
        name=product_model.name,
        description=product_model.description,
        unit_price=product_model.unit_price,
        cost_price=product_model.cost_price,
        unit_of_measure=product_model.unit_of_measure,
        tax_rate=product_model.tax_rate,
        is_taxable=product_model.is_taxable,
        track_inventory=product_model.track_inventory,
        quantity_in_stock=product_model.quantity_in_stock,
        low_stock_threshold=product_model.low_stock_threshold,
        image_url=product_model.image_url,
        is_active=product_model.is_active,
        created_at=product_model.created_at,
        updated_at=product_model.updated_at,
    )

@strawberry.type
class ProductQuery:
    @strawberry.field
    def product(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Product]:
        """Get product by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get product and verify user owns the business
        product = db.query(ProductModel).options(
            joinedload(ProductModel.business),
            joinedload(ProductModel.invoice_items)
        ).join(BusinessProfile).filter(
            ProductModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not product:
            return None
        
        return product_model_to_type(product)
    
    @strawberry.field
    def products(
        self,
        info: strawberry.Info,
        filter: Optional[ProductFilterInput] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Product]:
        """Get list of products with optional filters"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Base query - only products from user's businesses
        query = db.query(ProductModel).options(
            joinedload(ProductModel.business),
            joinedload(ProductModel.invoice_items)
        ).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id
        )
        
        # Apply filters
        if filter:
            if filter.business_id:
                query = query.filter(ProductModel.business_id == str(filter.business_id))
            
            if filter.name:
                query = query.filter(ProductModel.name.ilike(f"%{filter.name}%"))
            
            if filter.sku:
                query = query.filter(ProductModel.sku.ilike(f"%{filter.sku}%"))
            
            if filter.is_active is not None:
                query = query.filter(ProductModel.is_active == filter.is_active)
            
            if filter.track_inventory is not None:
                query = query.filter(ProductModel.track_inventory == filter.track_inventory)
            
            if filter.low_stock_only:
                query = query.filter(
                    ProductModel.track_inventory == True,
                    ProductModel.quantity_in_stock <= ProductModel.low_stock_threshold
                )
        
        # Order by name and apply pagination
        products = query.order_by(ProductModel.name).offset(skip).limit(limit).all()
        
        return [product_model_to_type(product) for product in products]
    
    @strawberry.field
    def products_by_business(
        self,
        info: strawberry.Info,
        business_id: strawberry.ID,
        skip: int = 0,
        limit: int = 10,
        active_only: bool = True,
    ) -> List[Product]:
        """Get products for a specific business"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business
        business = db.query(BusinessProfile).filter(
            BusinessProfile.id == str(business_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        query = db.query(ProductModel).options(
            joinedload(ProductModel.business),
            joinedload(ProductModel.invoice_items)
        ).filter(
            ProductModel.business_id == str(business_id)
        )
        
        if active_only:
            query = query.filter(ProductModel.is_active == True)
        
        products = query.order_by(ProductModel.name).offset(skip).limit(limit).all()
        
        return [product_model_to_type(product) for product in products]
    
    @strawberry.field
    def low_stock_products(
        self,
        info: strawberry.Info,
        business_id: Optional[strawberry.ID] = None,
    ) -> List[Product]:
        """Get products that are low in stock"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Base query - only products from user's businesses
        query = db.query(ProductModel).options(
            joinedload(ProductModel.business),
            joinedload(ProductModel.invoice_items)
        ).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id,
            ProductModel.track_inventory == True,
            ProductModel.is_active == True,
            ProductModel.quantity_in_stock <= ProductModel.low_stock_threshold
        )
        
        if business_id:
            query = query.filter(ProductModel.business_id == str(business_id))
        
        products = query.order_by(ProductModel.quantity_in_stock).all()
        
        return [product_model_to_type(product) for product in products]