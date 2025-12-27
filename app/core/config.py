from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"  # Default value
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Default value
    PYTOTP_SECRET_KEY: str = None
    # Other settings...
     # Mailtrap configuration
    MAILTRAP_API_KEY: str
    MAILTRAP_USE_SANDBOX: bool = True
    MAILTRAP_INBOX_ID: Optional[str] = None
    MAILTRAP_BULK_MODE: bool = False
    
    # Email defaults
    DEFAULT_SENDER_EMAIL: str = "noreply@invoicegen.com"
    DEFAULT_SENDER_NAME: str = "InvoiceGen"
    
    # Business email addresses
    INVOICE_SENDER_EMAIL: str = "invoices@invoicegen.com"
    INVOICE_SENDER_NAME: str = "InvoiceGen Invoices"
    
    QUOTE_SENDER_EMAIL: str = "quotes@invoicegen.com"
    QUOTE_SENDER_NAME: str = "InvoiceGen Quotes"
    
    REMINDER_SENDER_EMAIL: str = "reminders@invoicegen.com"
    REMINDER_SENDER_NAME: str = "InvoiceGen Reminders"
    
    SECURITY_SENDER_EMAIL: str = "security@invoicegen.com"
    SECURITY_SENDER_NAME: str = "InvoiceGen Security"
    
    SUPPORT_SENDER_EMAIL: str = "support@invoicegen.com"
    SUPPORT_SENDER_NAME: str = "InvoiceGen Support"
    
    # Environment
    EMAIL_ENVIRONMENT: str = None
    
    # Rate limiting
    EMAIL_RATE_LIMIT_PER_MINUTE: int = 100
    EMAIL_RATE_LIMIT_PER_HOUR: int = 1000
    REDIS_URL:str
    
    # Retry configuration
    EMAIL_MAX_RETRIES: int = 3
    EMAIL_RETRY_DELAY: int = 5  # seconds
    class Config:
        env_file = ".env"
        case_sensitive = False  # This allows lowercase env variables

settings = Settings()