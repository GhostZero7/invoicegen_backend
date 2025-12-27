"""
Email service configuration and environment management.

This module provides configuration management for the email service,
including environment variable handling, validation, and setup helpers.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseSettings, validator


class EmailEnvironment(str, Enum):
    """Email service environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class MailtrapConfig:
    """Mailtrap configuration data class."""
    api_token: str
    use_sandbox: bool = True
    inbox_id: Optional[str] = None
    bulk_mode: bool = False
    environment: EmailEnvironment = EmailEnvironment.DEVELOPMENT
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.use_sandbox and not self.inbox_id:
            raise ValueError("inbox_id is required when use_sandbox is True")
        
        if not self.api_token:
            raise ValueError("api_token is required")


class EmailSettings(BaseSettings):
    """Email service settings with environment variable support."""
    
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
    EMAIL_ENVIRONMENT: EmailEnvironment = EmailEnvironment.DEVELOPMENT
    
    # Rate limiting
    EMAIL_RATE_LIMIT_PER_MINUTE: int = 100
    EMAIL_RATE_LIMIT_PER_HOUR: int = 1000
    
    # Retry configuration
    EMAIL_MAX_RETRIES: int = 3
    EMAIL_RETRY_DELAY: int = 5  # seconds
    
    @validator('MAILTRAP_INBOX_ID')
    def validate_inbox_id(cls, v, values):
        """Validate inbox ID when sandbox mode is enabled."""
        if values.get('MAILTRAP_USE_SANDBOX', True) and not v:
            raise ValueError('MAILTRAP_INBOX_ID is required when MAILTRAP_USE_SANDBOX is True')
        return v
    
    @validator('MAILTRAP_API_KEY')
    def validate_api_key(cls, v):
        """Validate API key format."""
        if not v or len(v) < 10:
            raise ValueError('MAILTRAP_API_KEY must be a valid API key')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class EmailConfigManager:
    """Email configuration manager with environment-specific settings."""
    
    def __init__(self, settings: Optional[EmailSettings] = None):
        """Initialize configuration manager."""
        self.settings = settings or EmailSettings()
    
    def get_mailtrap_config(self) -> MailtrapConfig:
        """Get Mailtrap configuration."""
        return MailtrapConfig(
            api_token=self.settings.MAILTRAP_API_KEY,
            use_sandbox=self.settings.MAILTRAP_USE_SANDBOX,
            inbox_id=self.settings.MAILTRAP_INBOX_ID,
            bulk_mode=self.settings.MAILTRAP_BULK_MODE,
            environment=self.settings.EMAIL_ENVIRONMENT
        )
    
    def get_sender_config(self, email_type: str = "default") -> Dict[str, str]:
        """Get sender configuration for different email types."""
        sender_configs = {
            "default": {
                "email": self.settings.DEFAULT_SENDER_EMAIL,
                "name": self.settings.DEFAULT_SENDER_NAME
            },
            "invoice": {
                "email": self.settings.INVOICE_SENDER_EMAIL,
                "name": self.settings.INVOICE_SENDER_NAME
            },
            "quote": {
                "email": self.settings.QUOTE_SENDER_EMAIL,
                "name": self.settings.QUOTE_SENDER_NAME
            },
            "reminder": {
                "email": self.settings.REMINDER_SENDER_EMAIL,
                "name": self.settings.REMINDER_SENDER_NAME
            },
            "security": {
                "email": self.settings.SECURITY_SENDER_EMAIL,
                "name": self.settings.SECURITY_SENDER_NAME
            },
            "support": {
                "email": self.settings.SUPPORT_SENDER_EMAIL,
                "name": self.settings.SUPPORT_SENDER_NAME
            }
        }
        
        return sender_configs.get(email_type, sender_configs["default"])
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.settings.EMAIL_ENVIRONMENT == EmailEnvironment.PRODUCTION
    
    def is_sandbox_enabled(self) -> bool:
        """Check if sandbox mode is enabled."""
        return self.settings.MAILTRAP_USE_SANDBOX
    
    def get_rate_limits(self) -> Dict[str, int]:
        """Get rate limiting configuration."""
        return {
            "per_minute": self.settings.EMAIL_RATE_LIMIT_PER_MINUTE,
            "per_hour": self.settings.EMAIL_RATE_LIMIT_PER_HOUR
        }
    
    def get_retry_config(self) -> Dict[str, int]:
        """Get retry configuration."""
        return {
            "max_retries": self.settings.EMAIL_MAX_RETRIES,
            "retry_delay": self.settings.EMAIL_RETRY_DELAY
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate email configuration and return status."""
        issues = []
        warnings = []
        
        # Check required settings
        if not self.settings.MAILTRAP_API_KEY:
            issues.append("MAILTRAP_API_KEY is not set")
        
        if self.settings.MAILTRAP_USE_SANDBOX and not self.settings.MAILTRAP_INBOX_ID:
            issues.append("MAILTRAP_INBOX_ID is required for sandbox mode")
        
        # Check environment-specific settings
        if self.is_production():
            if self.settings.MAILTRAP_USE_SANDBOX:
                warnings.append("Sandbox mode is enabled in production environment")
            
            if "example.com" in self.settings.DEFAULT_SENDER_EMAIL:
                warnings.append("Using example.com domain in production")
        
        # Check rate limits
        if self.settings.EMAIL_RATE_LIMIT_PER_MINUTE > 1000:
            warnings.append("High rate limit per minute may cause issues")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "environment": self.settings.EMAIL_ENVIRONMENT.value,
            "sandbox_enabled": self.settings.MAILTRAP_USE_SANDBOX,
            "bulk_mode": self.settings.MAILTRAP_BULK_MODE
        }
    
    def generate_env_template(self) -> str:
        """Generate environment variable template."""
        return """
# Mailtrap Email Service Configuration
# ===================================

# Required: Your Mailtrap API token
# Get it from: https://mailtrap.io/api-tokens
MAILTRAP_API_KEY=your_api_token_here

# Sandbox mode (true for testing, false for production)
MAILTRAP_USE_SANDBOX=true

# Required for sandbox mode: Your inbox ID
# Get it from your Mailtrap inbox settings
MAILTRAP_INBOX_ID=your_inbox_id_here

# Optional: Enable bulk email mode
MAILTRAP_BULK_MODE=false

# Email sender configuration
DEFAULT_SENDER_EMAIL=noreply@yourdomain.com
DEFAULT_SENDER_NAME=Your Company Name

INVOICE_SENDER_EMAIL=invoices@yourdomain.com
INVOICE_SENDER_NAME=Your Company Invoices

QUOTE_SENDER_EMAIL=quotes@yourdomain.com
QUOTE_SENDER_NAME=Your Company Quotes

REMINDER_SENDER_EMAIL=reminders@yourdomain.com
REMINDER_SENDER_NAME=Your Company Reminders

SECURITY_SENDER_EMAIL=security@yourdomain.com
SECURITY_SENDER_NAME=Your Company Security

SUPPORT_SENDER_EMAIL=support@yourdomain.com
SUPPORT_SENDER_NAME=Your Company Support

# Environment (development, staging, production, testing)
EMAIL_ENVIRONMENT=development

# Rate limiting
EMAIL_RATE_LIMIT_PER_MINUTE=100
EMAIL_RATE_LIMIT_PER_HOUR=1000

# Retry configuration
EMAIL_MAX_RETRIES=3
EMAIL_RETRY_DELAY=5
"""


def setup_email_environment():
    """Interactive setup for email environment variables."""
    print("InvoiceGen Email Service Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"Found existing {env_file} file.")
        overwrite = input("Do you want to update email settings? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Collect configuration
    print("\nPlease provide the following information:")
    
    api_key = input("Mailtrap API Key: ").strip()
    if not api_key:
        print("API key is required. Get it from: https://mailtrap.io/api-tokens")
        return
    
    use_sandbox = input("Use sandbox mode? (y/n) [y]: ").lower().strip()
    use_sandbox = use_sandbox != 'n'
    
    inbox_id = ""
    if use_sandbox:
        inbox_id = input("Mailtrap Inbox ID: ").strip()
        if not inbox_id:
            print("Inbox ID is required for sandbox mode.")
            return
    
    sender_email = input("Default sender email [noreply@invoicegen.com]: ").strip()
    if not sender_email:
        sender_email = "noreply@invoicegen.com"
    
    sender_name = input("Default sender name [InvoiceGen]: ").strip()
    if not sender_name:
        sender_name = "InvoiceGen"
    
    # Generate configuration
    config_lines = [
        f"MAILTRAP_API_KEY={api_key}",
        f"MAILTRAP_USE_SANDBOX={'true' if use_sandbox else 'false'}",
    ]
    
    if inbox_id:
        config_lines.append(f"MAILTRAP_INBOX_ID={inbox_id}")
    
    config_lines.extend([
        f"DEFAULT_SENDER_EMAIL={sender_email}",
        f"DEFAULT_SENDER_NAME={sender_name}",
        "EMAIL_ENVIRONMENT=development"
    ])
    
    # Write to .env file
    if os.path.exists(env_file):
        # Read existing content
        with open(env_file, 'r') as f:
            existing_content = f.read()
        
        # Update or append email settings
        lines = existing_content.split('\n')
        updated_lines = []
        email_keys = {line.split('=')[0] for line in config_lines}
        
        # Update existing lines
        for line in lines:
            if '=' in line and line.split('=')[0] in email_keys:
                # Skip existing email settings, we'll add updated ones
                continue
            updated_lines.append(line)
        
        # Add email settings
        updated_lines.append("")
        updated_lines.append("# Email Service Configuration")
        updated_lines.extend(config_lines)
        
        with open(env_file, 'w') as f:
            f.write('\n'.join(updated_lines))
    else:
        # Create new .env file
        with open(env_file, 'w') as f:
            f.write("# Email Service Configuration\n")
            f.write('\n'.join(config_lines))
    
    print(f"\n✅ Email configuration saved to {env_file}")
    print("\nNext steps:")
    print("1. Test your configuration by running the email examples")
    print("2. Update sender email addresses to match your domain")
    print("3. Set EMAIL_ENVIRONMENT=production when ready for live emails")


if __name__ == "__main__":
    setup_email_environment()