"""Test GraphQL authentication"""

import asyncio
from app.graphql.schema import schema
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole, UserStatus
from app.auth.utils import create_access_token
from datetime import datetime

async def test_auth_graphql():
    # Create a test user in the database
    db = SessionLocal()
    
    try:
        # Create test user
        test_user = User(
            id="test-auth-user-123",
            email="testauth@example.com",
            password_hash="hashed_password",
            first_name="Auth",
            last_name="Test",
            phone="+1234567890",
            email_verified=True,
            two_factor_enabled=False,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            last_login_at=datetime.utcnow()
        )
        
        db.add(test_user)
        db.commit()
        
        # Create a JWT token for the user
        access_token = create_access_token(data={"sub": test_user.email})
        print(f"Generated token: {access_token[:50]}...")
        
        # Test the GraphQL query with authentication
        query = """
        query Me {
            me {
                id
                email
                firstName
                lastName
                role
            }
        }
        """
        
        # Mock the context with the authenticated user
        context = {
            "db": db,
            "current_user": test_user
        }
        
        result = await schema.execute(query, context_value=context)
        
        print("Query result:", result.data)
        if result.errors:
            print("Errors:", result.errors)
        else:
            print("✅ Authenticated GraphQL query executed successfully!")
            
        # Test without authentication
        context_no_auth = {
            "db": db,
            "current_user": None
        }
        
        result_no_auth = await schema.execute(query, context_value=context_no_auth)
        print("\nQuery result (no auth):", result_no_auth.data)
        if result_no_auth.errors:
            print("Errors (no auth):", result_no_auth.errors)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        db.query(User).filter(User.id == "test-auth-user-123").delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    asyncio.run(test_auth_graphql())