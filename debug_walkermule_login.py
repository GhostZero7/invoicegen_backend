
import sys
sys.path.append('.')
from app.db.database import SessionLocal
from app.db.models.user import User
from app.auth.utils import verify_password

def debug_user_login():
    db = SessionLocal()
    email = "walkermule7@gmail.com"
    password = "Mulenga@2004"
    
    print(f"--- Debugging login for {email} ---")
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print(f"FAILED: User '{email}' not found in database.")
        all_users = db.query(User.email).all()
        print(f"Available emails in DB: {[u.email for u in all_users]}")
    else:
        print(f"SUCCESS: User found. ID: {user.id}")
        print(f"Status: {user.status}")
        print(f"Email Verified: {user.email_verified}")
        
        match = verify_password(password, user.password_hash)
        if match:
            print("SUCCESS: Password matches stored hash.")
        else:
            print("FAILED: Password DOES NOT match stored hash.")
            
    db.close()

if __name__ == "__main__":
    debug_user_login()
