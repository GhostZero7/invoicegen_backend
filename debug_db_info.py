
import sys
from sqlalchemy import inspect
from app.db.database import engine
from app.core.config import settings

def debug_db():
    print("--- Database Debug Info ---")
    url = str(engine.url)
    # Mask password
    if ":" in url and "@" in url:
        part1 = url.split("@")[1]
        print(f"Connecting to: ...@{part1}")
    else:
        print(f"Connecting to: {url}")
        
    print(f"Config DATABASE_URL: {settings.DATABASE_URL}")

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\nFound {len(tables)} tables:")
    for table in tables:
        print(f" - {table}")
        
    if "verification_codes" in tables:
        print("\n 'verification_codes' table EXISTS.")
    else:
        print("\n 'verification_codes' table is MISSING.")

if __name__ == "__main__":
    debug_db()
