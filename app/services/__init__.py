"""
Services package for InvoiceGen application.

This package contains reusable business logic services including:
- Email service (Mailtrap integration)
- File upload service
- Notification service
- PDF generation service
"""

from .email_service import EmailService, EmailTemplate, EmailAttachment

__all__ = [
    "EmailService",
    "EmailTemplate", 
    "EmailAttachment"
]