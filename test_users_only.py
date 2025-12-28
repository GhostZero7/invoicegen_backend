"""Simple test to create just users"""
import sys
sys.path.append('.')

from app.db.database import SessionLocal
from app.db.models.user import User
from sqlalchemy import text

# Clear database first
db = SessionLocal()
db.execute(text('TRUNCATE TABLE users CASCADE'))
db.commit()
print("Database cleared")
db.close()

# Now try to create users
from seed_database import create_users

db = SessionLocal()
try:
    print("Creating users...")
    users = create_users(db)
    print(f"Successfully created {len(users)} users!")
    
    # Verify
    count = db.query(User).count()
    print(f"User count in DB: {count}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
