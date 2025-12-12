"""Test complete user flow with GraphQL"""

import asyncio
from app.graphql.schema import schema
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole, UserStatus
from datetime import datetime

async def test_complete_user_flow():
    # Create a test user in the database
    db = SessionLocal()
    
    try:
        # Create test user
        test_user = User(
            id="test-user-123",
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
            phone="+1234567890",
            email_verified=True,
            two_factor_enabled=False,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            last_login_at=datetime.utcnow()
        )
        
        db.add(test_user)
        db.commit()
        
        # Test the GraphQL query
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                email
                firstName
                lastName
                phone
                emailVerified
                twoFactorEnabled
                role
                status
                lastLoginAt
                createdAt
                updatedAt
            }
        }
        """
        
        variables = {"id": "test-user-123"}
        context = {"db": db}
        
        result = await schema.execute(query, variable_values=variables, context_value=context)
        
        print("Query result:", result.data)
        if result.errors:
            print("Errors:", result.errors)
        else:
            print("✅ GraphQL query executed successfully!")
            
        # Test users list query
        list_query = """
        query GetUsers {
            users(limit: 5) {
                id
                email
                firstName
                lastName
                role
                status
            }
        }
        """
        
        list_result = await schema.execute(list_query, context_value=context)
        print("\nUsers list result:", list_result.data)
        if list_result.errors:
            print("List errors:", list_result.errors)
        else:
            print("✅ Users list query executed successfully!")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        db.query(User).filter(User.id == "test-user-123").delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    asyncio.run(test_complete_user_flow())