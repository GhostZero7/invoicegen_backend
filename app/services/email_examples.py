"""
Email service usage examples for InvoiceGen.

This module demonstrates how to use the EmailService for various scenarios:
- Basic email sending
- Template-based emails
- Bulk email operations
- Invoice and quote emails
- Notification emails
"""

import os
from pathlib import Path
from typing import List

from .email_service import (
    EmailService,
    EmailMessage,
    EmailAddress,
    EmailTemplate,
    EmailAttachment,
    EmailCategory,
    EmailPriority,
    create_email_service
)


class EmailExamples:
    """Collection of email service usage examples."""
    
    def __init__(self):
        """Initialize with email service."""
        self.email_service = create_email_service()
    
    def basic_email_example(self):
        """Example: Send a basic email."""
        message = EmailMessage(
            sender=EmailAddress(email="sender@invoicegen.com", name="InvoiceGen"),
            to=[EmailAddress(email="recipient@example.com", name="John Doe")],
            subject="Welcome to InvoiceGen!",
            text="Thank you for joining InvoiceGen. We're excited to help you!",
            html="""
            <h1>Welcome to InvoiceGen!</h1>
            <p>Thank you for joining InvoiceGen. We're excited to help you!</p>
            """,
            category=EmailCategory.WELCOME
        )
        
        response = self.email_service.send_email(message)
        print(f"Email sent: {response}")
        return response
    
    def email_with_attachments_example(self):
        """Example: Send email with attachments."""
        # Create a sample PDF attachment
        pdf_content = b"Sample PDF content"  # In real use, this would be actual PDF bytes
        
        attachment = EmailAttachment(
            content=pdf_content,
            filename="sample.pdf",
            mimetype="application/pdf"
        )
        
        message = EmailMessage(
            sender=EmailAddress(email="invoices@invoicegen.com", name="InvoiceGen Invoices"),
            to=[EmailAddress(email="client@example.com", name="Jane Smith")],
            subject="Your Invoice #INV-001",
            text="Please find your invoice attached.",
            html="<p>Please find your invoice attached.</p>",
            attachments=[attachment],
            category=EmailCategory.INVOICE,
            priority=EmailPriority.HIGH
        )
        
        response = self.email_service.send_email(message)
        print(f"Email with attachment sent: {response}")
        return response
    
    def template_email_example(self):
        """Example: Send email using Mailtrap template."""
        template = EmailTemplate(
            template_uuid="your-template-uuid-here",
            template_variables={
                "user_name": "John Doe",
                "company_name": "Acme Corp",
                "invoice_number": "INV-001",
                "amount": "$1,500.00"
            }
        )
        
        response = self.email_service.send_template_email(
            sender=EmailAddress(email="noreply@invoicegen.com", name="InvoiceGen"),
            to=[EmailAddress(email="client@example.com", name="John Doe")],
            template=template,
            category=EmailCategory.INVOICE
        )
        
        print(f"Template email sent: {response}")
        return response
    
    def bulk_email_example(self):
        """Example: Send bulk emails."""
        # Create bulk email service
        bulk_service = create_email_service(bulk_mode=True)
        
        messages = []
        recipients = [
            ("client1@example.com", "Client One"),
            ("client2@example.com", "Client Two"),
            ("client3@example.com", "Client Three")
        ]
        
        for email, name in recipients:
            message = EmailMessage(
                sender=EmailAddress(email="newsletter@invoicegen.com", name="InvoiceGen Newsletter"),
                to=[EmailAddress(email=email, name=name)],
                subject="Monthly Newsletter",
                text=f"Hello {name}, here's your monthly newsletter!",
                html=f"<h1>Hello {name}</h1><p>Here's your monthly newsletter!</p>",
                category=EmailCategory.MARKETING
            )
            messages.append(message)
        
        responses = bulk_service.send_bulk_emails(messages)
        print(f"Bulk emails sent: {len(responses)} messages")
        return responses
    
    def invoice_email_example(self):
        """Example: Send invoice email with PDF."""
        # In real use, you'd generate the actual PDF
        invoice_pdf = b"Sample invoice PDF content"
        
        response = self.email_service.send_invoice_email(
            to_email="client@example.com",
            to_name="John Doe",
            invoice_number="INV-001",
            invoice_pdf=invoice_pdf
        )
        
        print(f"Invoice email sent: {response}")
        return response
    
    def quote_email_example(self):
        """Example: Send quote email with PDF."""
        # In real use, you'd generate the actual PDF
        quote_pdf = b"Sample quote PDF content"
        
        response = self.email_service.send_quote_email(
            to_email="prospect@example.com",
            to_name="Jane Smith",
            quote_number="QUO-001",
            quote_pdf=quote_pdf
        )
        
        print(f"Quote email sent: {response}")
        return response
    
    def payment_reminder_example(self):
        """Example: Send payment reminder."""
        response = self.email_service.send_payment_reminder(
            to_email="client@example.com",
            to_name="John Doe",
            invoice_number="INV-001",
            amount_due="$1,500.00",
            due_date="2024-01-15"
        )
        
        print(f"Payment reminder sent: {response}")
        return response
    
    def password_reset_example(self):
        """Example: Send password reset email."""
        reset_token = "abc123def456"
        reset_url = f"https://invoicegen.com/reset-password?token={reset_token}"
        
        response = self.email_service.send_password_reset_email(
            to_email="user@example.com",
            to_name="John Doe",
            reset_token=reset_token,
            reset_url=reset_url
        )
        
        print(f"Password reset email sent: {response}")
        return response
    
    def verification_email_example(self):
        """Example: Send email verification."""
        verification_token = "verify123abc456"
        verification_url = f"https://invoicegen.com/verify-email?token={verification_token}"
        
        response = self.email_service.send_verification_email(
            to_email="newuser@example.com",
            to_name="Jane Smith",
            verification_token=verification_token,
            verification_url=verification_url
        )
        
        print(f"Verification email sent: {response}")
        return response
    
    def multi_recipient_example(self):
        """Example: Send email to multiple recipients."""
        message = EmailMessage(
            sender=EmailAddress(email="announcements@invoicegen.com", name="InvoiceGen Announcements"),
            to=[
                EmailAddress(email="user1@example.com", name="User One"),
                EmailAddress(email="user2@example.com", name="User Two")
            ],
            cc=[EmailAddress(email="manager@invoicegen.com", name="Manager")],
            bcc=[EmailAddress(email="admin@invoicegen.com", name="Admin")],
            subject="System Maintenance Notice",
            text="We will be performing system maintenance on Sunday.",
            html="<p>We will be performing system maintenance on <strong>Sunday</strong>.</p>",
            category=EmailCategory.NOTIFICATION,
            priority=EmailPriority.HIGH
        )
        
        response = self.email_service.send_email(message)
        print(f"Multi-recipient email sent: {response}")
        return response
    
    def custom_headers_example(self):
        """Example: Send email with custom headers."""
        message = EmailMessage(
            sender=EmailAddress(email="system@invoicegen.com", name="InvoiceGen System"),
            to=[EmailAddress(email="user@example.com", name="User")],
            subject="Custom Headers Example",
            text="This email has custom headers.",
            headers={
                "X-Priority": "1",
                "X-MSMail-Priority": "High",
                "X-Mailer": "InvoiceGen Email Service",
                "X-Invoice-ID": "INV-001"
            },
            custom_variables={
                "campaign_id": "welcome_series",
                "user_segment": "premium"
            },
            category=EmailCategory.TRANSACTIONAL
        )
        
        response = self.email_service.send_email(message)
        print(f"Email with custom headers sent: {response}")
        return response


def run_all_examples():
    """Run all email examples."""
    print("Running InvoiceGen Email Service Examples")
    print("=" * 50)
    
    examples = EmailExamples()
    
    try:
        print("\n1. Basic Email Example:")
        examples.basic_email_example()
        
        print("\n2. Email with Attachments Example:")
        examples.email_with_attachments_example()
        
        print("\n3. Invoice Email Example:")
        examples.invoice_email_example()
        
        print("\n4. Quote Email Example:")
        examples.quote_email_example()
        
        print("\n5. Payment Reminder Example:")
        examples.payment_reminder_example()
        
        print("\n6. Password Reset Example:")
        examples.password_reset_example()
        
        print("\n7. Verification Email Example:")
        examples.verification_email_example()
        
        print("\n8. Multi-recipient Example:")
        examples.multi_recipient_example()
        
        print("\n9. Custom Headers Example:")
        examples.custom_headers_example()
        
        print("\n10. Bulk Email Example:")
        examples.bulk_email_example()
        
        print("\nAll examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have set the required environment variables:")
        print("- MAILTRAP_API_KEY")
        print("- MAILTRAP_USE_SANDBOX (optional, defaults to true)")
        print("- MAILTRAP_INBOX_ID (required for sandbox mode)")


if __name__ == "__main__":
    run_all_examples()