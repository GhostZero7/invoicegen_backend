
from app.db.database import Base, engine
from app.db.models.verification_code import VerificationCode
import sqlalchemy

def fix_table():
    print("Checking for verification_codes table...")
    inspector = sqlalchemy.inspect(engine)
    if "verification_codes" in inspector.get_table_names():
        print("Table 'verification_codes' already exists.")
    else:
        print("Table 'verification_codes' missing. Creating now...")
        # Create only the missing table
        VerificationCode.__table__.create(engine)
        print("Table 'verification_codes' created successfully.")

if __name__ == "__main__":
    try:
        fix_table()
    except Exception as e:
        print(f"Error creating table: {e}")
