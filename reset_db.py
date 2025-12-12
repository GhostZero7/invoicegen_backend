"""
Reset database script - drops all tables and recreates them
"""
import sys
import os
sys.path.append('.')

from sqlalchemy import text
from app.db.database import engine

def reset_database():
    """Drop all tables and recreate them"""
    print("Resetting database...")
    
    # Drop all tables
    print("Dropping all tables...")
    try:
        with engine.begin() as connection:
            # Drop tables in reverse order of dependencies
            connection.execute(text("DROP SCHEMA public CASCADE"))
            connection.execute(text("CREATE SCHEMA public"))
        print("Tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        return False
    
    # Create all tables
    print("Creating tables...")
    try:
        from app.db.database import Base
        from app.db.models.user import User
        from app.db.models.business import BusinessProfile
        from app.db.models.address import Address
        from app.db.models.client import Client, ClientContact
        from app.db.models.invoice import Invoice, InvoiceItem
        from app.db.models.product import Product
        
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if reset_database():
        print("\nDatabase reset complete!")
    else:
        print("\nDatabase reset failed!")
        sys.exit(1)


