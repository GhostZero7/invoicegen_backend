import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_verification_email(to_email: str, code: str):
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD
    smtp_from_email = settings.SMTP_FROM_EMAIL or smtp_username

    if not all([smtp_username, smtp_password]):
        print(" SMTP credentials not found. Email not sent.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your InvoiceGEN Verification Code"
    message["From"] = smtp_from_email
    message["To"] = to_email

    text = f"""
    Welcome to InvoiceGEN!
    
    Your verification code is: {code}
    
    This code will expire in 10 minutes.
    """

    html = f"""
    <html>
      <body>
        <h2>Welcome to InvoiceGEN!</h2>
        <p>Your verification code is:</p>
        <h1 style="color: #4F46E5; letter-spacing: 5px;">{code}</h1>
        <p>This code will expire in 10 minutes.</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_from_email, to_email, message.as_string())
        print(f" Email sent to {to_email}")
    except Exception as e:
        print(f" Error sending email: {e}")
        raise e # Re-raise to let the caller handle it
