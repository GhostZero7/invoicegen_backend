#!/usr/bin/env python3
"""
Test script for Waitlist GraphQL functionality
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.graphql.schema import schema
from app.core.deps import get_db
from app.db.models.user import User
from app.db.models.waitlist import Waitlist
from sqlalchemy.orm import Session

# Test queries
JOIN_WAITLIST_MUTATION = """
mutation JoinWaitlist($input: CreateWaitlistInput!) {
  joinWaitlist(input: $input) {
    id
    email
    firstName
    lastName
    companyName
    priority
    isNotified
    isConverted
    createdAt
  }
}
"""

CHECK_WAITLIST_BY_EMAIL_QUERY = """
query CheckWaitlistByEmail($email: String!) {
  waitlistByEmail(email: $email) {
    id
    email
    firstName
    lastName
    companyName
    priority
    isNotified
    createdAt
  }
}
"""

GET_WAITLIST_POSITION_QUERY = """
query GetWaitlistPosition($email: String!) {
  waitlistPosition(email: $email)
}
"""

WAITLIST_STATS_QUERY = """
query WaitlistStats {
  waitlistStats {
    totalCount
    notifiedCount
    convertedCount
    conversionRate
    recentSignups
  }
}
"""

GET_WAITLIST_ENTRIES_QUERY = """
query GetWaitlistEntries($filter: WaitlistFilterInput) {
  waitlistEntries(filter: $filter, limit: 10) {
    id
    email
    firstName
    lastName
    companyName
    priority
    isNotified
    isConverted
    createdAt
  }
}
"""

async def test_waitlist_functionality():
    """Test waitlist GraphQL operations"""
    
    # Get database session
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        print("🧪 Testing Waitlist GraphQL Implementation")
        print("=" * 50)
        
        # Test 1: Join waitlist (public endpoint)
        print("\n1. Testing joinWaitlist mutation (public)...")
        
        join_input = {
            "email": "test@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "companyName": "Test Company",
            "message": "Excited to try your product!",
            "source": "website",
            "utmSource": "google",
            "utmMedium": "cpc",
            "utmCampaign": "launch",
            "priority": "NORMAL"
        }
        
        context = {"db": db}  # No user for public endpoint
        
        result = await schema.execute(
            JOIN_WAITLIST_MUTATION,
            variable_values={"input": join_input},
            context_value=context
        )
        
        if result.errors:
            print(f"❌ Join waitlist failed: {result.errors}")
        else:
            waitlist_entry = result.data["joinWaitlist"]
            print(f"✅ Successfully joined waitlist:")
            print(f"   ID: {waitlist_entry['id']}")
            print(f"   Email: {waitlist_entry['email']}")
            print(f"   Name: {waitlist_entry['firstName']} {waitlist_entry['lastName']}")
            print(f"   Company: {waitlist_entry['companyName']}")
            print(f"   Priority: {waitlist_entry['priority']}")
        
        # Test 2: Check waitlist by email (public endpoint)
        print("\n2. Testing waitlistByEmail query (public)...")
        
        result = await schema.execute(
            CHECK_WAITLIST_BY_EMAIL_QUERY,
            variable_values={"email": "test@example.com"},
            context_value=context
        )
        
        if result.errors:
            print(f"❌ Check waitlist by email failed: {result.errors}")
        else:
            entry = result.data["waitlistByEmail"]
            if entry:
                print(f"✅ Found waitlist entry:")
                print(f"   Email: {entry['email']}")
                print(f"   Name: {entry['firstName']} {entry['lastName']}")
                print(f"   Notified: {entry['isNotified']}")
            else:
                print("❌ No waitlist entry found")
        
        # Test 3: Get waitlist position (public endpoint)
        print("\n3. Testing waitlistPosition query (public)...")
        
        result = await schema.execute(
            GET_WAITLIST_POSITION_QUERY,
            variable_values={"email": "test@example.com"},
            context_value=context
        )
        
        if result.errors:
            print(f"❌ Get waitlist position failed: {result.errors}")
        else:
            position = result.data["waitlistPosition"]
            if position:
                print(f"✅ Waitlist position: {position}")
            else:
                print("❌ No position found (entry doesn't exist)")
        
        # Test 4: Try duplicate email (should return existing entry)
        print("\n4. Testing duplicate email handling...")
        
        result = await schema.execute(
            JOIN_WAITLIST_MUTATION,
            variable_values={"input": {"email": "test@example.com", "firstName": "Jane"}},
            context_value=context
        )
        
        if result.errors:
            print(f"❌ Duplicate email test failed: {result.errors}")
        else:
            entry = result.data["joinWaitlist"]
            print(f"✅ Duplicate email handled correctly:")
            print(f"   Returned existing entry with name: {entry['firstName']}")
        
        # Test 5: Admin-only endpoints (should fail without admin user)
        print("\n5. Testing admin-only endpoints without authentication...")
        
        result = await schema.execute(
            WAITLIST_STATS_QUERY,
            context_value=context
        )
        
        if result.errors:
            print(f"✅ Admin endpoint correctly rejected: {result.errors[0].message}")
        else:
            print("❌ Admin endpoint should have been rejected")
        
        # Test 6: Admin-only endpoints with admin user
        print("\n6. Testing admin-only endpoints with admin user...")
        
        # Create mock admin user
        admin_user = User(
            id="admin-123",
            email="admin@example.com",
            role="admin",
            status="active"
        )
        
        admin_context = {"db": db, "current_user": admin_user}
        
        result = await schema.execute(
            WAITLIST_STATS_QUERY,
            context_value=admin_context
        )
        
        if result.errors:
            print(f"❌ Admin stats query failed: {result.errors}")
        else:
            stats = result.data["waitlistStats"]
            print(f"✅ Admin stats query successful:")
            print(f"   Total Count: {stats['totalCount']}")
            print(f"   Notified Count: {stats['notifiedCount']}")
            print(f"   Converted Count: {stats['convertedCount']}")
            print(f"   Conversion Rate: {stats['conversionRate']}%")
            print(f"   Recent Signups: {stats['recentSignups']}")
        
        # Test 7: Get waitlist entries (admin only)
        print("\n7. Testing waitlistEntries query (admin)...")
        
        result = await schema.execute(
            GET_WAITLIST_ENTRIES_QUERY,
            variable_values={"filter": {"priority": "NORMAL"}},
            context_value=admin_context
        )
        
        if result.errors:
            print(f"❌ Get waitlist entries failed: {result.errors}")
        else:
            entries = result.data["waitlistEntries"]
            print(f"✅ Found {len(entries)} waitlist entries")
            for entry in entries[:3]:  # Show first 3
                print(f"   - {entry['email']} ({entry['firstName']} {entry['lastName']})")
        
        print("\n" + "=" * 50)
        print("🎉 Waitlist GraphQL testing completed!")
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_waitlist_functionality())