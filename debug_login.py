
import sys
sys.path.append('.')

from app.db.database import SessionLocal
from app.db.models.user import User
from app.auth.utils import verify_password, hash_password

def check_login():
    db = SessionLocal()
    email = "accountant1@invoicegen.com"
    password = "Account123!"
    
    print(f"Checking login for: {email}")
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print("❌ User not found!")
        return
        
    print(f"User found: {user.id}")
    print(f"Stored hash: {user.password_hash}")
    
    is_valid = verify_password(password, user.password_hash)
    
    if is_valid:
        print("✅ Password valid!")
    else:
        print("❌ Password INVALID!")
        
        # Debugging: hash the password again and compare
        new_hash = hash_password(password)
        print(f"New hash of '{password}': {new_hash}")
        
    db.close()

if __name__ == "__main__":
    check_login()
