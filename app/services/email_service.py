"""
High-level reusable email service using Mailtrap SDK.

This service provides a comprehensive email solution with:
- Template-based emails
- Attachment support
- Sandbox/Production switching
- Bulk email capabilities
- Email tracking and analytics
- Error handling and retry logic
"""

import os
import base64
import logging
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

import mailtrap as mt
from pydantic import BaseModel, EmailStr, validator

# Configure logging
logger = logging.getLogger(__name__)


class EmailPriority(str, Enum):
    """Email priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class EmailCategory(str, Enum):
    """Email categories for tracking and analytics."""
    TRANSACTIONAL = "transactional"
    MARKETING = "marketing"
    NOTIFICATION = "notification"
    INVOICE = "invoice"
    QUOTE = "quote"
    REMINDER = "reminder"
    WELCOME = "welcome"
    PASSWORD_RESET = "password_reset"
    VERIFICATION = "verification"


@dataclass
class EmailAttachment:
    """Email attachment data class."""
    content: bytes
    filename: str
    mimetype: str
    disposition: mt.Disposition = mt.Disposition.ATTACHMENT
    content_id: Optional[str] = None
    
    def to_mailtrap_attachment(self) -> mt.Attachment:
        """Convert to Mailtrap attachment object."""
        return mt.Attachment(
            content=base64.b64encode(self.content),
            filename=self.filename,
            mimetype=self.mimetype,
            disposition=self.disposition,
            content_id=self.content_id
        )


class EmailAddress(BaseModel):
    """Email address with optional name."""
    email: EmailStr
    name: Optional[str] = None
    
    def to_mailtrap_address(self) -> mt.Address:
        """Convert to Mailtrap address object."""
        return mt.Address(email=str(self.email), name=self.name)


class EmailTemplate(BaseModel):
    """Email template configuration."""
    template_uuid: str
    template_variables: Dict[str, Any] = {}
    
    class Config:
        extra = "allow"


class EmailMessage(BaseModel):
    """Email message configuration."""
    sender: EmailAddress
    to: List[EmailAddress]
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    cc: Optional[List[EmailAddress]] = None
    bcc: Optional[List[EmailAddress]] = None
    attachments: Optional[List[EmailAttachment]] = None
    headers: Optional[Dict[str, str]] = None
    custom_variables: Optional[Dict[str, Any]] = None
    category: EmailCategory = EmailCategory.TRANSACTIONAL
    priority: EmailPriority = EmailPriority.NORMAL
    
    @validator('to', 'cc', 'bcc')
    def validate_email_lists(cls, v):
        """Ensure email lists are not empty if provided."""
        if v is not None and len(v) == 0:
            raise ValueError("Email list cannot be empty if provided")
        return v
    
    @validator('text', 'html')
    def validate_content(cls, v, values):
        """Ensure at least one content type is provided."""
        if not v and not values.get('html') and not values.get('text'):
            raise ValueError("Either text or html content must be provided")
        return v


class EmailService:
    """
    High-level email service using Mailtrap SDK.
    
    Features:
    - Environment-based configuration
    - Sandbox/Production switching
    - Template support
    - Bulk email capabilities
    - Error handling and retry logic
    - Email tracking
    """
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        use_sandbox: Optional[bool] = None,
        inbox_id: Optional[str] = None,
        bulk_mode: bool = False
    ):
        """
        Initialize email service.
        
        Args:
            api_token: Mailtrap API token (defaults to env var)
            use_sandbox: Use sandbox mode (defaults to env var)
            inbox_id: Sandbox inbox ID (defaults to env var)
            bulk_mode: Enable bulk email mode
        """
        # Load configuration from environment or parameters
        self.api_token = api_token or os.environ.get("MAILTRAP_API_KEY")
        self.use_sandbox = (
            use_sandbox if use_sandbox is not None 
            else os.environ.get("MAILTRAP_USE_SANDBOX", "true").lower() == "true"
        )
        self.inbox_id = inbox_id or os.environ.get("MAILTRAP_INBOX_ID")
        self.bulk_mode = bulk_mode
        
        if not self.api_token:
            raise ValueError("MAILTRAP_API_KEY environment variable or api_token parameter is required")
        
        # Initialize Mailtrap client
        self.client = mt.MailtrapClient(
            token=self.api_token,
            sandbox=self.use_sandbox,
            inbox_id=self.inbox_id if self.use_sandbox else None,
            bulk=self.bulk_mode
        )
        
        logger.info(f"EmailService initialized - Sandbox: {self.use_sandbox}, Bulk: {self.bulk_mode}")
    
    def send_email(self, message: EmailMessage) -> Dict[str, Any]:
        """
        Send a single email message.
        
        Args:
            message: Email message configuration
            
        Returns:
            Dict containing success status and message IDs
            
        Raises:
            Exception: If email sending fails
        """
        try:
            # Convert to Mailtrap mail object
            mail = self._create_mail_object(message)
            
            # Send email
            response = self.client.send(mail)
            
            logger.info(f"Email sent successfully to {[addr.email for addr in message.to]}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
    
    def send_template_email(
        self,
        sender: EmailAddress,
        to: List[EmailAddress],
        template: EmailTemplate,
        cc: Optional[List[EmailAddress]] = None,
        bcc: Optional[List[EmailAddress]] = None,
        category: EmailCategory = EmailCategory.TRANSACTIONAL
    ) -> Dict[str, Any]:
        """
        Send email using a Mailtrap template.
        
        Args:
            sender: Sender email address
            to: List of recipient email addresses
            template: Email template configuration
            cc: Optional CC recipients
            bcc: Optional BCC recipients
            category: Email category for tracking
            
        Returns:
            Dict containing success status and message IDs
        """
        try:
            # Create template mail object
            mail = mt.MailFromTemplate(
                sender=sender.to_mailtrap_address(),
                to=[addr.to_mailtrap_address() for addr in to],
                cc=[addr.to_mailtrap_address() for addr in cc] if cc else None,
                bcc=[addr.to_mailtrap_address() for addr in bcc] if bcc else None,
                template_uuid=template.template_uuid,
                template_variables=template.template_variables,
                category=category.value
            )
            
            # Send email
            response = self.client.send(mail)
            
            logger.info(f"Template email sent successfully to {[addr.email for addr in to]}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            raise
    
    def send_bulk_emails(self, messages: List[EmailMessage]) -> List[Dict[str, Any]]:
        """
        Send multiple emails in bulk.
        
        Args:
            messages: List of email messages
            
        Returns:
            List of response dictionaries
        """
        if not self.bulk_mode:
            logger.warning("Bulk mode not enabled, sending emails individually")
            return [self.send_email(msg) for msg in messages]
        
        try:
            # Convert messages to mail objects
            mails = [self._create_mail_object(msg) for msg in messages]
            
            # Send bulk emails
            response = self.client.batch_send(mails)
            
            logger.info(f"Bulk emails sent successfully: {len(messages)} messages")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send bulk emails: {str(e)}")
            raise
    
    def _create_mail_object(self, message: EmailMessage) -> mt.Mail:
        """Create Mailtrap Mail object from EmailMessage."""
        # Convert attachments
        attachments = None
        if message.attachments:
            attachments = [att.to_mailtrap_attachment() for att in message.attachments]
        
        # Create mail object
        mail = mt.Mail(
            sender=message.sender.to_mailtrap_address(),
            to=[addr.to_mailtrap_address() for addr in message.to],
            cc=[addr.to_mailtrap_address() for addr in message.cc] if message.cc else None,
            bcc=[addr.to_mailtrap_address() for addr in message.bcc] if message.bcc else None,
            subject=message.subject,
            text=message.text,
            html=message.html,
            attachments=attachments,
            headers=message.headers,
            custom_variables=message.custom_variables,
            category=message.category.value
        )
        
        return mail
    
    # Convenience methods for common email types
    
    def send_welcome_email(
        self,
        to_email: str,
        to_name: str,
        sender_email: str = "noreply@invoicegen.com",
        sender_name: str = "InvoiceGen"
    ) -> Dict[str, Any]:
        """Send welcome email to new user."""
        message = EmailMessage(
            sender=EmailAddress(email=sender_email, name=sender_name),
            to=[EmailAddress(email=to_email, name=to_name)],
            subject="Welcome to InvoiceGen!",
            html=self._get_welcome_email_html(to_name),
            text=f"Welcome to InvoiceGen, {to_name}! Thank you for joining us.",
            category=EmailCategory.WELCOME
        )
        return self.send_email(message)
    
    def send_invoice_email(
        self,
        to_email: str,
        to_name: str,
        invoice_number: str,
        invoice_pdf: bytes,
        sender_email: str = "invoices@invoicegen.com",
        sender_name: str = "InvoiceGen Invoices"
    ) -> Dict[str, Any]:
        """Send invoice email with PDF attachment."""
        attachment = EmailAttachment(
            content=invoice_pdf,
            filename=f"invoice_{invoice_number}.pdf",
            mimetype="application/pdf"
        )
        
        message = EmailMessage(
            sender=EmailAddress(email=sender_email, name=sender_name),
            to=[EmailAddress(email=to_email, name=to_name)],
            subject=f"Invoice #{invoice_number}",
            html=self._get_invoice_email_html(to_name, invoice_number),
            text=f"Dear {to_name}, please find attached invoice #{invoice_number}.",
            attachments=[attachment],
            category=EmailCategory.INVOICE,
            priority=EmailPriority.HIGH
        )
        return self.send_email(message)
    
    def send_quote_email(
        self,
        to_email: str,
        to_name: str,
        quote_number: str,
        quote_pdf: bytes,
        sender_email: str = "quotes@invoicegen.com",
        sender_name: str = "InvoiceGen Quotes"
    ) -> Dict[str, Any]:
        """Send quote email with PDF attachment."""
        attachment = EmailAttachment(
            content=quote_pdf,
            filename=f"quote_{quote_number}.pdf",
            mimetype="application/pdf"
        )
        
        message = EmailMessage(
            sender=EmailAddress(email=sender_email, name=sender_name),
            to=[EmailAddress(email=to_email, name=to_name)],
            subject=f"Quote #{quote_number}",
            html=self._get_quote_email_html(to_name, quote_number),
            text=f"Dear {to_name}, please find attached quote #{quote_number}.",
            attachments=[attachment],
            category=EmailCategory.QUOTE,
            priority=EmailPriority.HIGH
        )
        return self.send_email(message)
    
    def send_payment_reminder(
        self,
        to_email: str,
        to_name: str,
        invoice_number: str,
        amount_due: str,
        due_date: str,
        sender_email: str = "reminders@invoicegen.com",
        sender_name: str = "InvoiceGen Reminders"
    ) -> Dict[str, Any]:
        """Send payment reminder email."""
        message = EmailMessage(
            sender=EmailAddress(email=sender_email, name=sender_name),
            to=[EmailAddress(email=to_email, name=to_name)],
            subject=f"Payment Reminder - Invoice #{invoice_number}",
            html=self._get_reminder_email_html(to_name, invoice_number, amount_due, due_date),
            text=f"Dear {to_name}, this is a reminder that invoice #{invoice_number} for {amount_due} is due on {due_date}.",
            category=EmailCategory.REMINDER,
            priority=EmailPriority.HIGH
        )
        return self.send_email(message)
    
    def send_password_reset_email(
        self,
        to_email: str,
        to_name: str,
        reset_token: str,
        reset_url: str,
        sender_email: str = "security@invoicegen.com",
        sender_name: str = "InvoiceGen Security"
    ) -> Dict[str, Any]:
        """Send password reset email."""
        message = EmailMessage(
            sender=EmailAddress(email=sender_email, name=sender_name),
            to=[EmailAddress(email=to_email, name=to_name)],
            subject="Password Reset Request",
            html=self._get_password_reset_email_html(to_name, reset_url),
            text=f"Dear {to_name}, click this link to reset your password: {reset_url}",
            category=EmailCategory.PASSWORD_RESET,
            priority=EmailPriority.HIGH
        )
        return self.send_email(message)
    
    def send_verification_email(
        self,
        to_email: str,
        to_name: str,
        verification_token: str,
        verification_url: str,
        sender_email: str = "verify@invoicegen.com",
        sender_name: str = "InvoiceGen Verification"
    ) -> Dict[str, Any]:
        """Send email verification email."""
        message = EmailMessage(
            sender=EmailAddress(email=sender_email, name=sender_name),
            to=[EmailAddress(email=to_email, name=to_name)],
            subject="Verify Your Email Address",
            html=self._get_verification_email_html(to_name, verification_url),
            text=f"Dear {to_name}, click this link to verify your email: {verification_url}",
            category=EmailCategory.VERIFICATION,
            priority=EmailPriority.HIGH,
            
        )
        return self.send_email(message)
    
    # HTML email templates
    
    def _get_welcome_email_html(self, name: str) -> str:
        """Get welcome email HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to InvoiceGen</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Welcome to InvoiceGen!</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {name}!</h2>
                <p>Thank you for joining InvoiceGen. We're excited to help you streamline your invoicing and financial management.</p>
                <p>Here's what you can do with InvoiceGen:</p>
                <ul style="padding-left: 20px;">
                    <li>Create professional invoices and quotes</li>
                    <li>Manage clients and products</li>
                    <li>Track payments and expenses</li>
                    <li>Generate financial reports</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://invoicegen.com/dashboard" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Get Started</a>
                </div>
                <p>If you have any questions, feel free to contact our support team.</p>
                <p>Best regards,<br>The InvoiceGen Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_invoice_email_html(self, name: str, invoice_number: str) -> str:
        """Get invoice email HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Invoice #{invoice_number}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #2c3e50; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Invoice #{invoice_number}</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Dear {name},</h2>
                <p>Please find attached your invoice #{invoice_number}.</p>
                <p>You can review the invoice details in the attached PDF document.</p>
                <div style="background: #e8f4fd; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Payment Instructions:</strong></p>
                    <p style="margin: 5px 0;">Please process payment according to the terms specified in the invoice.</p>
                </div>
                <p>If you have any questions about this invoice, please don't hesitate to contact us.</p>
                <p>Thank you for your business!</p>
                <p>Best regards,<br>The InvoiceGen Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_quote_email_html(self, name: str, quote_number: str) -> str:
        """Get quote email HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quote #{quote_number}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #27ae60; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Quote #{quote_number}</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Dear {name},</h2>
                <p>Thank you for your interest in our services. Please find attached your quote #{quote_number}.</p>
                <p>This quote is valid for 30 days from the date of issue.</p>
                <div style="background: #d5f4e6; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Next Steps:</strong></p>
                    <p style="margin: 5px 0;">If you'd like to proceed, please let us know and we'll convert this quote to an invoice.</p>
                </div>
                <p>If you have any questions about this quote, please feel free to contact us.</p>
                <p>We look forward to working with you!</p>
                <p>Best regards,<br>The InvoiceGen Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_reminder_email_html(self, name: str, invoice_number: str, amount_due: str, due_date: str) -> str:
        """Get payment reminder email HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Payment Reminder</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #e74c3c; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Payment Reminder</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Dear {name},</h2>
                <p>This is a friendly reminder that payment for invoice #{invoice_number} is due.</p>
                <div style="background: #ffeaa7; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Payment Details:</strong></p>
                    <p style="margin: 5px 0;">Invoice: #{invoice_number}</p>
                    <p style="margin: 5px 0;">Amount Due: {amount_due}</p>
                    <p style="margin: 5px 0;">Due Date: {due_date}</p>
                </div>
                <p>Please process your payment at your earliest convenience to avoid any late fees.</p>
                <p>If you have already made this payment, please disregard this reminder.</p>
                <p>If you have any questions or concerns, please contact us immediately.</p>
                <p>Thank you for your prompt attention to this matter.</p>
                <p>Best regards,<br>The InvoiceGen Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_password_reset_email_html(self, name: str, reset_url: str) -> str:
        """Get password reset email HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #f39c12; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Password Reset</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {name},</h2>
                <p>We received a request to reset your password for your InvoiceGen account.</p>
                <p>Click the button below to reset your password:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background: #f39c12; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a>
                </div>
                <p>If you didn't request this password reset, please ignore this email. Your password will remain unchanged.</p>
                <p>This link will expire in 1 hour for security reasons.</p>
                <p>Best regards,<br>The InvoiceGen Security Team</p>
            </div>
        </body>
        </html>
        """
    
    def _get_verification_email_html(self, name: str, verification_url: str) -> str:
        """Get email verification HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: #9b59b6; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Verify Your Email</h1>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {name},</h2>
                <p>Thank you for signing up for InvoiceGen! To complete your registration, please verify your email address.</p>
                <p>Use the code below to verify your email:</p>
                <div style="text-align: center; margin: 30px 0;">
                   {verification_url}
                </div>
                <p>If you didn't create an account with InvoiceGen, please ignore this email.</p>
                <p>This verification link will expire in 24 hours.</p>
                <p>Best regards,<br>The InvoiceGen Team</p>
            </div>
        </body>
        </html>
        """


# Factory function for easy service creation
def create_email_service(
    api_token: Optional[str] = None,
    use_sandbox: Optional[bool] = None,
    inbox_id: Optional[str] = None,
    bulk_mode: bool = False
) -> EmailService:
    """
    Factory function to create EmailService instance.
    
    Args:
        api_token: Mailtrap API token
        use_sandbox: Use sandbox mode
        inbox_id: Sandbox inbox ID
        bulk_mode: Enable bulk email mode
        
    Returns:
        Configured EmailService instance
    """
    return EmailService(
        api_token=api_token,
        use_sandbox=use_sandbox,
        inbox_id=inbox_id,
        bulk_mode=bulk_mode
    )