#!/usr/bin/env python3
"""
Create waitlist table in the database
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import Base, engine
from app.db.models.waitlist import Waitlist

def create_waitlist_table():
    """Create the waitlist table"""
    print("🔧 Creating waitlist table...")
    
    try:
        # Create only the waitlist table
        Waitlist.__table__.create(engine, checkfirst=True)
        print("✅ Waitlist table created successfully!")
        
        # Verify table exists
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'waitlists' in tables:
            print("✅ Waitlist table verified in database")
            
            # Show table columns
            columns = inspector.get_columns('waitlists')
            print(f"📋 Table has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
        else:
            print("❌ Waitlist table not found in database")
            
    except Exception as e:
        print(f"❌ Error creating waitlist table: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_waitlist_table()