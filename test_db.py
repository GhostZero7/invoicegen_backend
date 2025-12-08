# test_db.py
from sqlalchemy import create_engine, text

# Use the same connection string from your .env
DATABASE_URL = "postgresql://mulenga:Mulenga%402004@localhost:5432/invoicegen"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("PostgreSQL version:", result.fetchone()[0])
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")