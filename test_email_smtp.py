
from dotenv import load_dotenv
import os
import sys

# Load env from current directory
load_dotenv(".env")

sys.path.append(".")

from app.utils.email import send_verification_email

if __name__ == "__main__":
    email = "mulengamusamba72@gmail.com"
    code = "123456"
    print(f"Attempting to send email to {email} using:")
    print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
    print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
    print(f"SMTP_USERNAME: {os.getenv('SMTP_USERNAME')}")
    
    try:
        send_verification_email(email, code)
        print("Test finished successfully.")
    except Exception as e:
        print(f"Test failed: {e}")
