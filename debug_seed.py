import sys
import traceback
sys.path.append('.')
from seed_database import seed_database
from app.db.database import SessionLocal
from app.db.models.user import User

def main():
    db = SessionLocal()
    count = db.query(User).count()
    print(f"Initial user count: {count}")
    db.close()
    
    try:
        seed_database()
        print("Success!")
    except Exception as e:
        print("\n" + "="*50)
        print("SEEDING FAILED")
        print("="*50)
        traceback.print_exc()
        print("="*50)
        sys.exit(1)

if __name__ == "__main__":
    main()
