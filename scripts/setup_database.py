#!/usr/bin/env python3
"""
Database Setup Script for InvoiceGen
=====================================

This script handles:
1. Database creation
2. Table creation
3. Admin user creation
4. Initial data seeding
5. SSL configuration handling

Usage:
    python scripts/setup_database.py [options]

Options:
    --create-db     Create the database if it doesn't exist
    --create-admin  Create an admin user
    --seed-data     Seed initial data
    --reset         Drop and recreate all tables
    --ssl-mode      Set SSL mode (disable/require/prefer)
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError, ProgrammingError
from app.db.database import Base, SessionLocal
from app.auth.utils import hash_password, generate_user_id
from app.core.config import settings

# Import all models to ensure they're registered
from app.db.models.user import User, UserStatus
from app.db.models.business import BusinessProfile, BusinessType
from app.db.models.categories import Category, CategoryType
from app.db.models.client import Client, ClientStatus
from app.db.models.product import Product
from app.db.models.invoice import Invoice
from app.db.models.address import Address, AddressType
from app.db.models.waitlist import Waitlist
from app.db.models.tax_rate import TaxRate
from app.db.models.expense import Expense
from app.db.models.payment import Payment
from app.db.models.qoute import Quote
from app.db.models.notification import Notification
from app.db.models.invoice_reminder import InvoiceReminder
from app.db.models.audit_log import AuditLog

def get_database_url_without_db(database_url: str) -> tuple[str, str]:
    """Extract database name and return URL without database name."""
    if "postgresql://" in database_url:
        # Split URL to get database name
        parts = database_url.split("/")
        db_name = parts[-1].split("?")[0]  # Remove query parameters
        base_url = "/".join(parts[:-1])
        return base_url, db_name
    return database_url, "invoicegen"

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    print("🔍 Checking if database exists...")
    
    base_url, db_name = get_database_url_without_db(settings.DATABASE_URL)
    
    # Connect to postgres database to create our target database
    postgres_url = f"{base_url}/postgres"
    
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )
            
            if not result.fetchone():
                print(f"📦 Creating database '{db_name}'...")
                # Need to commit the transaction and create database outside transaction
                conn.execute(text("COMMIT"))
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"✅ Database '{db_name}' created successfully!")
            else:
                print(f"✅ Database '{db_name}' already exists.")
                
    except OperationalError as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("💡 Make sure PostgreSQL is running and credentials are correct.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def create_tables():
    """Create all database tables."""
    print("🏗️  Creating database tables...")
    
    try:
        from app.db.database import engine
        
        # Configure SQLAlchemy registry to resolve relationships
        from sqlalchemy.orm import configure_mappers
        configure_mappers()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def drop_all_tables():
    """Drop all database tables."""
    print("🗑️  Dropping all tables...")
    
    try:
        from app.db.database import engine
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return False

def create_admin_user():
    """Create an admin user."""
    print("👤 Creating admin user...")
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@invoicegen.com").first()
        if existing_admin:
            print("✅ Admin user already exists.")
            return True
        
        # Create admin user
        admin_user = User(
            id=generate_user_id(),
            email="admin@invoicegen.com",
            username="admin",
            first_name="Admin",
            last_name="User",
            password_hash=hash_password("admin123"),  # Change this password!
            is_active=True,
            is_verified=True,
            status=UserStatus.ACTIVE,
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Admin user created successfully!")
        print("📧 Email: admin@invoicegen.com")
        print("🔑 Password: admin123")
        print("⚠️  Please change the admin password after first login!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def seed_initial_data():
    """Seed the database with initial data."""
    print("🌱 Seeding initial data...")
    
    db = SessionLocal()
    try:
        # Create default categories
        categories_data = [
            {"name": "General", "type": CategoryType.PRODUCT, "description": "General products"},
            {"name": "Services", "type": CategoryType.PRODUCT, "description": "Service-based products"},
            {"name": "Office Supplies", "type": CategoryType.EXPENSE, "description": "Office supplies and equipment"},
            {"name": "Travel", "type": CategoryType.EXPENSE, "description": "Travel and transportation expenses"},
            {"name": "Marketing", "type": CategoryType.EXPENSE, "description": "Marketing and advertising expenses"},
        ]
        
        for cat_data in categories_data:
            existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
        
        # Create default tax rates
        tax_rates_data = [
            {"name": "No Tax", "rate": 0.0, "is_default": False},
            {"name": "Standard VAT", "rate": 20.0, "is_default": True},
            {"name": "Reduced VAT", "rate": 5.0, "is_default": False},
        ]
        
        for tax_data in tax_rates_data:
            existing = db.query(TaxRate).filter(TaxRate.name == tax_data["name"]).first()
            if not existing:
                tax_rate = TaxRate(**tax_data)
                db.add(tax_rate)
        
        db.commit()
        print("✅ Initial data seeded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def update_ssl_mode(ssl_mode: str):
    """Update SSL mode in environment files."""
    print(f"🔒 Updating SSL mode to: {ssl_mode}")
    
    env_files = [".env", ".env.local"]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                
                # Update DATABASE_URL with new SSL mode
                lines = content.split('\n')
                updated_lines = []
                
                for line in lines:
                    if line.startswith('DATABASE_URL='):
                        # Extract the URL and update SSL mode
                        url = line.split('=', 1)[1].strip('"')
                        if '?' in url:
                            base_url, params = url.split('?', 1)
                            # Remove existing sslmode parameter
                            param_pairs = [p for p in params.split('&') if not p.startswith('sslmode=')]
                            # Add new sslmode
                            param_pairs.append(f'sslmode={ssl_mode}')
                            new_url = f'{base_url}?{"&".join(param_pairs)}'
                        else:
                            new_url = f'{url}?sslmode={ssl_mode}'
                        
                        updated_lines.append(f'DATABASE_URL="{new_url}"')
                    else:
                        updated_lines.append(line)
                
                with open(env_file, 'w') as f:
                    f.write('\n'.join(updated_lines))
                
                print(f"✅ Updated {env_file}")
                
            except Exception as e:
                print(f"❌ Error updating {env_file}: {e}")

def check_database_connection():
    """Test database connection."""
    print("🔌 Testing database connection...")
    
    try:
        from app.db.database import engine
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.fetchone():
                print("✅ Database connection successful!")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="InvoiceGen Database Setup")
    parser.add_argument("--create-db", action="store_true", help="Create database if it doesn't exist")
    parser.add_argument("--create-admin", action="store_true", help="Create admin user")
    parser.add_argument("--seed-data", action="store_true", help="Seed initial data")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables")
    parser.add_argument("--ssl-mode", choices=["disable", "require", "prefer"], help="Set SSL mode")
    parser.add_argument("--all", action="store_true", help="Run all setup steps")
    
    args = parser.parse_args()
    
    print("🚀 InvoiceGen Database Setup")
    print("=" * 40)
    
    # Update SSL mode if specified
    if args.ssl_mode:
        update_ssl_mode(args.ssl_mode)
        print("🔄 Please restart the application to use the new SSL settings.")
        return
    
    # Test database connection first
    if not check_database_connection():
        print("💡 Try running with --ssl-mode disable if you're using a local database")
        return
    
    success = True
    
    # Create database if requested
    if args.create_db or args.all:
        success &= create_database_if_not_exists()
    
    # Reset tables if requested
    if args.reset:
        success &= drop_all_tables()
        success &= create_tables()
    elif args.all:
        success &= create_tables()
    
    # Create admin user if requested
    if args.create_admin or args.all:
        success &= create_admin_user()
    
    # Seed data if requested
    if args.seed_data or args.all:
        success &= seed_initial_data()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n❌ Database setup completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()