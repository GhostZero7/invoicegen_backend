import sys
import os

sys.path.append(os.getcwd())

try:
    print("Importing VerificationCode...")
    from app.db.models.verification_code import VerificationCode
    print("✅ VerificationCode imported.")
except Exception as e:
    print(f"❌ Failed to import VerificationCode: {e}")

try:
    print("Importing send_verification_email...")
    from app.utils.email import send_verification_email
    print("✅ send_verification_email imported.")
except Exception as e:
    print(f"❌ Failed to import email utils: {e}")
