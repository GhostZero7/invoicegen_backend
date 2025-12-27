"""Test Product GraphQL functionality"""

import asyncio
from app.graphql.schema import schema
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole, UserStatus
from app.db.models.business import BusinessProfile, BusinessType, PaymentTerms
from app.db.models.product import Product
from datetime import datetime
import uuid

async def test_product_graphql():
    db = SessionLocal()
    
    try:
        # Create test user
        test_user = User(
            id="test-product-user-123",
            email="producttest@example.com",
            password_hash="hashed_password",
            first_name="Product",
            last_name="Tester",
            phone="+1234567890",
            email_verified=True,
            two_factor_enabled=False,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            last_login_at=datetime.utcnow()
        )
        
        db.add(test_user)
        db.flush()
        
        # Create test business
        test_business = BusinessProfile(
            id="test-business-123",
            user_id=test_user.id,
            business_name="Test Product Business",
            business_type=BusinessType.LLC,
            email="business@example.com",
            currency="USD",
            timezone="UTC",
            payment_terms_default=PaymentTerms.NET_30,
            is_active=True,
            created_at=datetime.utcnow().date(),
            updated_at=datetime.utcnow().date()
        )
        
        db.add(test_business)
        db.commit()
        
        # Test create product mutation
        create_mutation = """
        mutation CreateProduct($input: CreateProductInput!) {
            createProduct(input: $input) {
                id
                name
                sku
                unitPrice
                isActive
                businessId
            }
        }
        """
        
        create_variables = {
            "input": {
                "businessId": test_business.id,
                "name": "Test Product",
                "sku": "TEST-001",
                "unitPrice": 99.99,
                "description": "A test product",
                "unitOfMeasure": "piece",
                "taxRate": 10.0,
                "isTaxable": True,
                "trackInventory": True,
                "quantityInStock": 100,
                "lowStockThreshold": 10
            }
        }
        
        context = {
            "db": db,
            "current_user": test_user
        }
        
        result = await schema.execute(create_mutation, variable_values=create_variables, context_value=context)
        
        if result.errors:
            print("Create Product Errors:", result.errors)
        else:
            print("✅ Create Product Success:", result.data)
            product_id = result.data["createProduct"]["id"]
            
            # Test get products query
            products_query = """
            query GetProducts($businessId: ID!) {
                productsByBusiness(businessId: $businessId) {
                    id
                    name
                    sku
                    unitPrice
                    quantityInStock
                    isActive
                }
            }
            """
            
            products_variables = {
                "businessId": test_business.id
            }
            
            products_result = await schema.execute(products_query, variable_values=products_variables, context_value=context)
            
            if products_result.errors:
                print("Get Products Errors:", products_result.errors)
            else:
                print("✅ Get Products Success:", products_result.data)
            
            # Test update product mutation
            update_mutation = """
            mutation UpdateProduct($id: ID!, $input: UpdateProductInput!) {
                updateProduct(id: $id, input: $input) {
                    id
                    name
                    unitPrice
                    quantityInStock
                }
            }
            """
            
            update_variables = {
                "id": product_id,
                "input": {
                    "unitPrice": 149.99,
                    "quantityInStock": 75
                }
            }
            
            update_result = await schema.execute(update_mutation, variable_values=update_variables, context_value=context)
            
            if update_result.errors:
                print("Update Product Errors:", update_result.errors)
            else:
                print("✅ Update Product Success:", update_result.data)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        db.query(Product).filter(Product.business_id == "test-business-123").delete()
        db.query(BusinessProfile).filter(BusinessProfile.id == "test-business-123").delete()
        db.query(User).filter(User.id == "test-product-user-123").delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    asyncio.run(test_product_graphql())