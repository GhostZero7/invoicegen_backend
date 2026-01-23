#!/usr/bin/env python3
"""
Test Business API Endpoints
Tests the new business profile API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8080"
TEST_EMAIL = "walkermule7@gmail.com"
TEST_PASSWORD = "User123!"

def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"✅ Login successful, token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_get_business_profiles(token):
    """Test getting business profiles"""
    print("\n📋 Testing GET /business...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/business", headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        businesses = response.json()
        print(f"✅ Found {len(businesses)} business profiles")
        for business in businesses:
            print(f"  - {business['business_name']} ({business['business_type']})")
            print(f"    ID: {business['id']}")
            print(f"    Email: {business['email']}")
            print(f"    Active: {business['is_active']}")
        return businesses
    else:
        print(f"❌ Failed: {response.text}")
        return []

def test_get_single_business(token, business_id):
    """Test getting a single business profile"""
    print(f"\n🏢 Testing GET /business/{business_id}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/business/{business_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        business = response.json()
        print(f"✅ Business details:")
        print(f"  - Name: {business['business_name']}")
        print(f"  - Type: {business['business_type']}")
        print(f"  - Email: {business['email']}")
        print(f"  - Phone: {business['phone']}")
        print(f"  - Currency: {business['currency']}")
        print(f"  - Invoice Prefix: {business['invoice_prefix']}")
        return business
    else:
        print(f"❌ Failed: {response.text}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing Business Profile API Endpoints")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        return
    
    # Test getting all business profiles
    businesses = test_get_business_profiles(token)
    
    # Test getting a single business profile
    if businesses:
        business_id = businesses[0]['id']
        test_get_single_business(token, business_id)
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()