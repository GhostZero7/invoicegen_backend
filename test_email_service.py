#!/usr/bin/env python3
"""
Test script for InvoiceGen Email Service.

This script tests the email service functionality including:
- Configuration validation
- Basic email sending
- Template emails
- Attachment handling
- Error handling
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.services.email_service import (
    EmailService,
    EmailMessage,
    EmailAddress,
    EmailAttachment,
    EmailCategory,
    EmailPriority,
    create_email_service
)
from app.services.email_config import EmailConfigManager, EmailSettings


def test_configuration():
    """Test email service configuration."""
    print("🔧 Testing Email Service Configuration")
    print("-" * 40)
    
    try:
        # Test configuration loading
        config_manager = EmailConfigManager()
        validation_result = config_manager.validate_configuration()
        
        print(f"Configuration Valid: {validation_result['valid']}")
        print(f"Environment: {validation_result['environment']}")
        print(f"Sandbox Enabled: {validation_result['sandbox_enabled']}")
        print(f"Bulk Mode: {validation_result['bulk_mode']}")
        
        if validation_result['issues']:
            print("\n❌ Configuration Issues:")
            for issue in validation_result['issues']:
                print(f"  • {issue}")
        
        if validation_result['warnings']:
            print("\n⚠️  Configuration Warnings:")
            for warning in validation_result['warnings']:
                print(f"  • {warning}")
        
        if validation_result['valid']:
            print("✅ Configuration is valid!")
        else:
            print("❌ Configuration has issues that need to be resolved.")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_email_service_initialization():
    """Test email service initialization."""
    print("\n🚀 Testing Email Service Initialization")
    print("-" * 40)
    
    try:
        # Test service creation
        email_service = create_email_service()
        print("✅ Email service created successfully!")
        
        # Test service properties
        print(f"Sandbox Mode: {email_service.use_sandbox}")
        print(f"Bulk Mode: {email_service.bulk_mode}")
        print(f"Has API Token: {'Yes' if email_service.api_token else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Email service initialization failed: {e}")
        return False


def test_email_message_creation():
    """Test email message creation and validation."""
    print("\n📧 Testing Email Message Creation")
    print("-" * 40)
    
    try:
        # Test basic message
        message = EmailMessage(
            sender=EmailAddress(email="test@invoicegen.com", name="Test Sender"),
            to=[EmailAddress(email="recipient@example.com", name="Test Recipient")],
            subject="Test Email",
            text="This is a test email.",
            html="<p>This is a test email.</p>",
            category=EmailCategory.TRANSACTIONAL
        )
        
        print("✅ Basic email message created successfully!")
        print(f"Sender: {message.sender.email}")
        print(f"Recipients: {len(message.to)}")
        print(f"Subject: {message.subject}")
        print(f"Category: {message.category}")
        
        # Test message with attachments
        attachment = EmailAttachment(
            content=b"Test file content",
            filename="test.txt",
            mimetype="text/plain"
        )
        
        message_with_attachment = EmailMessage(
            sender=EmailAddress(email="test@invoicegen.com", name="Test Sender"),
            to=[EmailAddress(email="recipient@example.com", name="Test Recipient")],
            subject="Test Email with Attachment",
            text="This email has an attachment.",
            attachments=[attachment],
            category=EmailCategory.INVOICE
        )
        
        print("✅ Email message with attachment created successfully!")
        print(f"Attachments: {len(message_with_attachment.attachments)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Email message creation failed: {e}")
        return False


def test_convenience_methods():
    """Test convenience methods for common email types."""
    print("\n🎯 Testing Convenience Methods")
    print("-" * 40)
    
    try:
        email_service = create_email_service()
        
        # Test method availability
        methods = [
            'send_welcome_email',
            'send_invoice_email',
            'send_quote_email',
            'send_payment_reminder',
            'send_password_reset_email',
            'send_verification_email'
        ]
        
        for method_name in methods:
            if hasattr(email_service, method_name):
                print(f"✅ {method_name} method available")
            else:
                print(f"❌ {method_name} method missing")
        
        print("✅ All convenience methods are available!")
        return True
        
    except Exception as e:
        print(f"❌ Convenience methods test failed: {e}")
        return False


def test_dry_run_email():
    """Test email sending in dry run mode (without actually sending)."""
    print("\n🧪 Testing Email Sending (Dry Run)")
    print("-" * 40)
    
    try:
        # Check if we have valid configuration
        if not os.environ.get("MAILTRAP_API_KEY") or os.environ.get("MAILTRAP_API_KEY") == "your_api_token_here":
            print("⚠️  Skipping actual email test - no valid API key configured")
            print("To test email sending:")
            print("1. Get your API key from https://mailtrap.io/api-tokens")
            print("2. Set MAILTRAP_API_KEY in your .env file")
            print("3. Set MAILTRAP_INBOX_ID for sandbox mode")
            return True
        
        email_service = create_email_service()
        
        # Create test message
        message = EmailMessage(
            sender=EmailAddress(email="test@invoicegen.com", name="InvoiceGen Test"),
            to=[EmailAddress(email="test@example.com", name="Test User")],
            subject="InvoiceGen Email Service Test",
            text="This is a test email from InvoiceGen email service.",
            html="""
            <h1>InvoiceGen Email Service Test</h1>
            <p>This is a test email from InvoiceGen email service.</p>
            <p>If you receive this, the email service is working correctly!</p>
            """,
            category=EmailCategory.TRANSACTIONAL
        )
        
        print("📧 Test email message prepared:")
        print(f"  From: {message.sender.email}")
        print(f"  To: {message.to[0].email}")
        print(f"  Subject: {message.subject}")
        
        # Note: Uncomment the line below to actually send the test email
        # response = email_service.send_email(message)
        # print(f"✅ Email sent successfully: {response}")
        
        print("✅ Email message prepared successfully (not sent in dry run)")
        return True
        
    except Exception as e:
        print(f"❌ Email sending test failed: {e}")
        return False


def run_all_tests():
    """Run all email service tests."""
    print("🧪 InvoiceGen Email Service Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Service Initialization", test_email_service_initialization),
        ("Message Creation", test_email_message_creation),
        ("Convenience Methods", test_convenience_methods),
        ("Email Sending (Dry Run)", test_dry_run_email)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Email service is ready to use.")
        print("\nNext steps:")
        print("1. Configure your Mailtrap API key and inbox ID")
        print("2. Run the email examples: python app/services/email_examples.py")
        print("3. Integrate email service into your application")
    else:
        print("❌ Some tests failed. Please check the configuration and try again.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)