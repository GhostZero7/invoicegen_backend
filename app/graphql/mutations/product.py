import strawberry
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.graphql.types.product import Product, CreateProductInput, UpdateProductInput
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
class ProductMutation:
    @strawberry.mutation
    async def create_product(self, info: strawberry.Info, input: CreateProductInput) -> Product:
        """Create a new product"""
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
        
        # Check if SKU is unique (if provided)
        if input.sku:
            existing_product = db.query(ProductModel).filter(
                ProductModel.sku == input.sku,
                ProductModel.business_id == str(input.business_id)
            ).first()
            
            if existing_product:
                raise Exception("Product with this SKU already exists")
        
        # Create the product
        product = ProductModel(
            id=str(uuid.uuid4()),
            business_id=str(input.business_id),
            sku=input.sku,
            name=input.name,
            description=input.description,
            unit_price=input.unit_price,
            cost_price=input.cost_price,
            unit_of_measure=input.unit_of_measure,
            tax_rate=input.tax_rate,
            is_taxable=input.is_taxable,
            track_inventory=input.track_inventory,
            quantity_in_stock=input.quantity_in_stock,
            low_stock_threshold=input.low_stock_threshold,
            image_url=input.image_url,
            is_active=True,
            created_at=datetime.utcnow().date(),
            updated_at=datetime.utcnow().date()
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        return product_model_to_type(product)
    
    @strawberry.mutation
    async def update_product(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdateProductInput
    ) -> Product:
        """Update an existing product"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get product and verify user owns the business
        product = db.query(ProductModel).join(BusinessProfile).filter(
            ProductModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not product:
            raise Exception("Product not found")
        
        # Check if SKU is unique (if being updated)
        if input.sku and input.sku != product.sku:
            existing_product = db.query(ProductModel).filter(
                ProductModel.sku == input.sku,
                ProductModel.business_id == product.business_id,
                ProductModel.id != str(id)
            ).first()
            
            if existing_product:
                raise Exception("Product with this SKU already exists")
        
        # Update fields
        if input.sku is not None:
            product.sku = input.sku
        if input.name is not None:
            product.name = input.name
        if input.description is not None:
            product.description = input.description
        if input.unit_price is not None:
            product.unit_price = input.unit_price
        if input.cost_price is not None:
            product.cost_price = input.cost_price
        if input.unit_of_measure is not None:
            product.unit_of_measure = input.unit_of_measure
        if input.tax_rate is not None:
            product.tax_rate = input.tax_rate
        if input.is_taxable is not None:
            product.is_taxable = input.is_taxable
        if input.track_inventory is not None:
            product.track_inventory = input.track_inventory
        if input.quantity_in_stock is not None:
            product.quantity_in_stock = input.quantity_in_stock
        if input.low_stock_threshold is not None:
            product.low_stock_threshold = input.low_stock_threshold
        if input.image_url is not None:
            product.image_url = input.image_url
        if input.is_active is not None:
            product.is_active = input.is_active
        
        product.updated_at = datetime.utcnow().date()
        
        db.commit()
        db.refresh(product)
        
        return product_model_to_type(product)
    
    @strawberry.mutation
    async def delete_product(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a product (soft delete by setting is_active to False)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get product and verify user owns the business
        product = db.query(ProductModel).join(BusinessProfile).filter(
            ProductModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not product:
            raise Exception("Product not found")
        
        # Soft delete by setting is_active to False
        product.is_active = False
        product.updated_at = datetime.utcnow().date()
        
        db.commit()
        
        return True
    
    @strawberry.mutation
    async def update_product_stock(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        quantity: int,
        operation: str = "set"  # "set", "add", "subtract"
    ) -> Product:
        """Update product stock quantity"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get product and verify user owns the business
        product = db.query(ProductModel).join(BusinessProfile).filter(
            ProductModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not product:
            raise Exception("Product not found")
        
        if not product.track_inventory:
            raise Exception("Product does not track inventory")
        
        # Update stock based on operation
        if operation == "set":
            product.quantity_in_stock = quantity
        elif operation == "add":
            product.quantity_in_stock += quantity
        elif operation == "subtract":
            product.quantity_in_stock = max(0, product.quantity_in_stock - quantity)
        else:
            raise Exception("Invalid operation. Use 'set', 'add', or 'subtract'")
        
        product.updated_at = datetime.utcnow().date()
        
        db.commit()
        db.refresh(product)
        
        return product_model_to_type(product)
    
    @strawberry.mutation
    async def duplicate_product(self, info: strawberry.Info, id: strawberry.ID) -> Product:
        """Duplicate an existing product"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get original product and verify user owns the business
        original_product = db.query(ProductModel).join(BusinessProfile).filter(
            ProductModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not original_product:
            raise Exception("Product not found")
        
        # Create duplicate with modified name and no SKU
        duplicate_product = ProductModel(
            id=str(uuid.uuid4()),
            business_id=original_product.business_id,
            sku=None,  # Clear SKU to avoid conflicts
            name=f"{original_product.name} (Copy)",
            description=original_product.description,
            unit_price=original_product.unit_price,
            cost_price=original_product.cost_price,
            unit_of_measure=original_product.unit_of_measure,
            tax_rate=original_product.tax_rate,
            is_taxable=original_product.is_taxable,
            track_inventory=original_product.track_inventory,
            quantity_in_stock=0,  # Start with 0 stock
            low_stock_threshold=original_product.low_stock_threshold,
            image_url=original_product.image_url,
            is_active=True,
            created_at=datetime.utcnow().date(),
            updated_at=datetime.utcnow().date()
        )
        
        db.add(duplicate_product)
        db.commit()
        db.refresh(duplicate_product)
        
        return product_model_to_type(duplicate_product)