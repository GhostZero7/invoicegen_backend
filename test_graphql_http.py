"""Test GraphQL over HTTP with authentication"""

import requests
import json
from app.auth.utils import create_access_token
from app.db.database import SessionLocal
from app.db.models.user import User

def test_graphql_http():
    # Get an existing user from the database
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if not user:
            print("No users found in database")
            return
        
        # Create a JWT token for the user
        access_token = create_access_token(data={"sub": user.email})
        print(f"Testing with user: {user.email}")
        print(f"Generated token: {access_token[:50]}...")
        
        # Test GraphQL query over HTTP
        url = "http://localhost:8000/graphql"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
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
        
        payload = {
            "query": query
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data", {}).get("me"):
                    print("✅ Authentication working correctly!")
                else:
                    print("❌ Authentication failed - user is None")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server. Make sure the backend is running on http://localhost:8000")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test_graphql_http()