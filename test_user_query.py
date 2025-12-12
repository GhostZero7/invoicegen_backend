"""Test the specific user query that was failing"""

import asyncio
from app.graphql.schema import schema
from app.db.database import SessionLocal

async def test_user_query():
    query = """
    query Users($id: ID!) {
        user(id: $id) {
            phone
            firstName
            lastName
            lastLoginAt
            twoFactorEnabled
            role
            status
            updatedAt
            email
            emailVerified
            avatarUrl
            id
        }
    }
    """
    
    variables = {"id": "fa1fac0e-48f4-44da-845e-471b8b3c5bf2"}
    
    # Create a mock context as a dictionary
    context = {
        "db": SessionLocal()
    }
    
    try:
        result = await schema.execute(query, variable_values=variables, context_value=context)
        print("Query result:", result.data)
        if result.errors:
            print("Errors:", result.errors)
    except Exception as e:
        print(f"Error executing query: {e}")
        import traceback
        traceback.print_exc()
    finally:
        context["db"].close()

if __name__ == "__main__":
    asyncio.run(test_user_query())