#!/usr/bin/env python3
"""
Test Business Profile GraphQL endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "walkermule@gmail.com",
            "password": "password123"
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login successful! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_graphql_business_queries(token):
    """Test GraphQL business queries"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📋 Testing GraphQL Business Queries")
    print("=" * 50)
    
    # Test 1: Get my businesses
    print("\n1️⃣ Testing myBusinesses query...")
    query = """
    query GetMyBusinesses {
      myBusinesses {
        id
        businessName
        businessType
        email
        currency
        isActive
        createdAt
      }
    }
    """
    
    response = requests.post(
        f"{BASE_URL}/graphql",
        json={"query": query},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            print(f"❌ GraphQL errors: {data['errors']}")
        else:
            businesses = data.get("data", {}).get("myBusinesses", [])
            print(f"✅ Found {len(businesses)} businesses")
            for business in businesses:
                print(f"   - {business['businessName']} ({business['businessType']})")
    else:
        print(f"❌ Request failed: {response.status_code} - {response.text}")
    
    # Test 2: Get specific business (if we have any)
    if response.status_code == 200:
        data = response.json()
        businesses = data.get("data", {}).get("myBusinesses", [])
        if businesses:
            business_id = businesses[0]["id"]
            print(f"\n2️⃣ Testing business query for ID: {business_id}")
            
            query = """
            query GetBusiness($id: ID!) {
              business(id: $id) {
                id
                businessName
                businessType
                taxId
                email
                phone
                currency
                invoicePrefix
                isActive
              }
            }
            """
            
            response = requests.post(
                f"{BASE_URL}/graphql",
                json={
                    "query": query,
                    "variables": {"id": business_id}
                },
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    print(f"❌ GraphQL errors: {data['errors']}")
                else:
                    business = data.get("data", {}).get("business")
                    if business:
                        print(f"✅ Business details retrieved:")
                        print(f"   - Name: {business['businessName']}")
                        print(f"   - Type: {business['businessType']}")
                        print(f"   - Email: {business['email']}")
                        print(f"   - Currency: {business['currency']}")
                    else:
                        print("❌ Business not found")
            else:
                print(f"❌ Request failed: {response.status_code} - {response.text}")

def test_graphql_business_mutations(token):
    """Test GraphQL business mutations"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🔧 Testing GraphQL Business Mutations")
    print("=" * 50)
    
    # Test create business
    print("\n1️⃣ Testing createBusiness mutation...")
    mutation = """
    mutation CreateBusiness($input: CreateBusinessInput!) {
      createBusiness(input: $input) {
        id
        businessName
        businessType
        email
        currency
        invoicePrefix
        isActive
      }
    }
    """
    
    input_data = {
        "businessName": "Test GraphQL Business",
        "businessType": "LLC",
        "email": "test@graphql.com",
        "currency": "USD",
        "invoicePrefix": "TEST"
    }
    
    response = requests.post(
        f"{BASE_URL}/graphql",
        json={
            "query": mutation,
            "variables": {"input": input_data}
        },
        headers=headers
    )
    
    created_business_id = None
    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            print(f"❌ GraphQL errors: {data['errors']}")
        else:
            business = data.get("data", {}).get("createBusiness")
            if business:
                created_business_id = business["id"]
                print(f"✅ Business created successfully!")
                print(f"   - ID: {business['id']}")
                print(f"   - Name: {business['businessName']}")
                print(f"   - Type: {business['businessType']}")
            else:
                print("❌ Business creation failed")
    else:
        print(f"❌ Request failed: {response.status_code} - {response.text}")
    
    # Test update business (if created successfully)
    if created_business_id:
        print(f"\n2️⃣ Testing updateBusiness mutation for ID: {created_business_id}")
        
        mutation = """
        mutation UpdateBusiness($id: ID!, $input: UpdateBusinessInput!) {
          updateBusiness(id: $id, input: $input) {
            id
            businessName
            businessType
            website
            phone
          }
        }
        """
        
        update_data = {
            "businessName": "Updated GraphQL Business",
            "website": "https://updated.example.com",
            "phone": "+1-555-0123"
        }
        
        response = requests.post(
            f"{BASE_URL}/graphql",
            json={
                "query": mutation,
                "variables": {
                    "id": created_business_id,
                    "input": update_data
                }
            },
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"❌ GraphQL errors: {data['errors']}")
            else:
                business = data.get("data", {}).get("updateBusiness")
                if business:
                    print(f"✅ Business updated successfully!")
                    print(f"   - Name: {business['businessName']}")
                    print(f"   - Website: {business['website']}")
                    print(f"   - Phone: {business['phone']}")
                else:
                    print("❌ Business update failed")
        else:
            print(f"❌ Request failed: {response.status_code} - {response.text}")
        
        # Test delete business
        print(f"\n3️⃣ Testing deleteBusiness mutation for ID: {created_business_id}")
        
        mutation = """
        mutation DeleteBusiness($id: ID!) {
          deleteBusiness(id: $id)
        }
        """
        
        response = requests.post(
            f"{BASE_URL}/graphql",
            json={
                "query": mutation,
                "variables": {"id": created_business_id}
            },
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"❌ GraphQL errors: {data['errors']}")
            else:
                result = data.get("data", {}).get("deleteBusiness")
                if result:
                    print(f"✅ Business deleted successfully!")
                else:
                    print("❌ Business deletion failed")
        else:
            print(f"❌ Request failed: {response.status_code} - {response.text}")

def main():
    """Main test function"""
    print("🧪 Testing Business Profile GraphQL Endpoints")
    print("=" * 50)
    
    # Login first
    token = login()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test queries
    test_graphql_business_queries(token)
    
    # Test mutations
    test_graphql_business_mutations(token)
    
    print("\n🎉 GraphQL Business Profile tests completed!")

if __name__ == "__main__":
    main()