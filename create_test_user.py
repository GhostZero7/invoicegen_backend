"""
Quick script to create a test user in the database
Run this to create a user you can login with
"""
import sys
sys.path.append('.')

from app.db.database import SessionLocal
from app.db.models.user import User
from app.auth.utils import hash_password
from datetime import datetime

def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.email == "test@example.com").first()
        if existing:
            print("✅ Test user already exists!")
            print(f"Email: test@example.com")
            print(f"Password: Test123!")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            password_hash=hash_password("Test123!"),
            first_name="Test",
            last_name="User",
            role="user",
            status="active",
            email_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print(f"\nLogin credentials:")
        print(f"Email: test@example.com")
        print(f"Password: Test123!")
        print(f"\nUser ID: {test_user.id}")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
