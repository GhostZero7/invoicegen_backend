import sys
import os
sys.path.append('.')

from app.db.database import engine, Base
from app.db.models.verification_code import VerificationCode

def create_table():
    print("Creating verification_codes table...")
    try:
        # distinct call to create just this table if possible, or all (idempotent)
        VerificationCode.__table__.create(engine)
        print("✅ Table 'verification_codes' created successfully!")
    except Exception as e:
        print(f"⚠️ Error creating table (might already exist?): {e}")
        # fallback to create_all
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ create_all executed.")
        except Exception as e2:
             print(f"❌ create_all failed: {e2}")

if __name__ == "__main__":
    create_table()
