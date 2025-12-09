# test_neon.py
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Neon PostgreSQL version:", result.fetchone()[0])
        print("✅ Connected to Neon successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")