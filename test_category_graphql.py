"""Test Category GraphQL functionality"""

import asyncio
from app.graphql.schema import schema
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole, UserStatus
from app.db.models.business import BusinessProfile, BusinessType, PaymentTerms
from app.db.models.categories import Category, CategoryType
from datetime import datetime
import uuid

async def test_category_graphql():
    db = SessionLocal()
    
    try:
        # Create test user
        test_user = User(
            id="test-category-user-123",
            email="categorytest@example.com",
            password_hash="hashed_password",
            first_name="Category",
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
            id="test-business-cat-123",
            user_id=test_user.id,
            business_name="Test Category Business",
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
        
        # Test create category mutation
        create_mutation = """
        mutation CreateCategory($input: CreateCategoryInput!) {
            createCategory(input: $input) {
                id
                name
                categoryType
                businessId
                sortOrder
                isActive
            }
        }
        """
        
        create_variables = {
            "input": {
                "businessId": test_business.id,
                "name": "Electronics",
                "description": "Electronic products category",
                "categoryType": "PRODUCT",
                "color": "#FF5733",
                "icon": "electronics",
                "sortOrder": 1
            }
        }
        
        context = {
            "db": db,
            "current_user": test_user
        }
        
        result = await schema.execute(create_mutation, variable_values=create_variables, context_value=context)
        
        if result.errors:
            print("Create Category Errors:", result.errors)
        else:
            print("✅ Create Category Success:", result.data)
            parent_category_id = result.data["createCategory"]["id"]
            
            # Create subcategory
            subcategory_variables = {
                "input": {
                    "businessId": test_business.id,
                    "name": "Smartphones",
                    "description": "Mobile phones and smartphones",
                    "categoryType": "PRODUCT",
                    "parentId": parent_category_id,
                    "color": "#33FF57",
                    "icon": "smartphone",
                    "sortOrder": 1
                }
            }
            
            subcategory_result = await schema.execute(create_mutation, variable_values=subcategory_variables, context_value=context)
            
            if subcategory_result.errors:
                print("Create Subcategory Errors:", subcategory_result.errors)
            else:
                print("✅ Create Subcategory Success:", subcategory_result.data)
            
            # Test get categories query
            categories_query = """
            query GetCategories($businessId: ID!, $categoryType: CategoryType!) {
                categoriesByBusiness(businessId: $businessId, categoryType: $categoryType) {
                    id
                    name
                    description
                    color
                    icon
                    parentId
                    sortOrder
                    isActive
                }
            }
            """
            
            categories_variables = {
                "businessId": test_business.id,
                "categoryType": "PRODUCT"
            }
            
            categories_result = await schema.execute(categories_query, variable_values=categories_variables, context_value=context)
            
            if categories_result.errors:
                print("Get Categories Errors:", categories_result.errors)
            else:
                print("✅ Get Categories Success:", categories_result.data)
            
            # Test category tree query
            tree_query = """
            query GetCategoryTree($businessId: ID!, $categoryType: CategoryType!) {
                categoryTree(businessId: $businessId, categoryType: $categoryType) {
                    id
                    name
                    color
                    icon
                    subcategories {
                        id
                        name
                        color
                        icon
                        parentId
                    }
                }
            }
            """
            
            tree_result = await schema.execute(tree_query, variable_values=categories_variables, context_value=context)
            
            if tree_result.errors:
                print("Get Category Tree Errors:", tree_result.errors)
            else:
                print("✅ Get Category Tree Success:", tree_result.data)
            
            # Test update category mutation
            update_mutation = """
            mutation UpdateCategory($id: ID!, $input: UpdateCategoryInput!) {
                updateCategory(id: $id, input: $input) {
                    id
                    name
                    description
                    color
                    sortOrder
                }
            }
            """
            
            update_variables = {
                "id": parent_category_id,
                "input": {
                    "description": "Updated electronics category description",
                    "color": "#FF3357",
                    "sortOrder": 2
                }
            }
            
            update_result = await schema.execute(update_mutation, variable_values=update_variables, context_value=context)
            
            if update_result.errors:
                print("Update Category Errors:", update_result.errors)
            else:
                print("✅ Update Category Success:", update_result.data)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        db.query(Category).filter(Category.business_id == "test-business-cat-123").delete()
        db.query(BusinessProfile).filter(BusinessProfile.id == "test-business-cat-123").delete()
        db.query(User).filter(User.id == "test-category-user-123").delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    asyncio.run(test_category_graphql())