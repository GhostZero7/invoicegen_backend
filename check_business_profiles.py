#!/usr/bin/env python3
"""
Check Business Profiles Script
Checks if there are users with business profiles in the database
"""

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.user import User
from app.db.models.business import BusinessProfile

def check_business_profiles():
    """Check users with business profiles"""
    print("\n--- Checking Business Profiles ---")
    
    db = SessionLocal()
    
    try:
        # Get all users
        users = db.query(User).all()
        print(f"Total users in database: {len(users)}")
        
        # Get all business profiles
        business_profiles = db.query(BusinessProfile).all()
        print(f"Total business profiles: {len(business_profiles)}")
        
        if business_profiles:
            print("\n--- Business Profiles Found ---")
            for bp in business_profiles:
                user = db.query(User).filter(User.id == bp.user_id).first()
                print(f"Business: {bp.business_name}")
                print(f"  - ID: {bp.id}")
                print(f"  - Owner: {user.email if user else 'Unknown'} ({user.first_name} {user.last_name})")
                print(f"  - Type: {bp.business_type}")
                print(f"  - Email: {bp.email}")
                print(f"  - Phone: {bp.phone}")
                print(f"  - Currency: {bp.currency}")
                print(f"  - Invoice Prefix: {bp.invoice_prefix}")
                print(f"  - Active: {bp.is_active}")
                print(f"  - Created: {bp.created_at}")
                print()
        else:
            print("\n❌ No business profiles found in database")
            
        # Check specific user (walkermule7@gmail.com)
        walker_user = db.query(User).filter(User.email == "walkermule7@gmail.com").first()
        if walker_user:
            walker_business = db.query(BusinessProfile).filter(BusinessProfile.user_id == walker_user.id).first()
            print(f"\n--- Walker User Business Profile ---")
            print(f"User: {walker_user.email}")
            if walker_business:
                print(f"✅ Has business profile: {walker_business.business_name}")
                print(f"  - Business ID: {walker_business.id}")
                print(f"  - Type: {walker_business.business_type}")
                print(f"  - Active: {walker_business.is_active}")
            else:
                print("❌ No business profile found for walker user")
        else:
            print("\n❌ Walker user not found in database")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_business_profiles()