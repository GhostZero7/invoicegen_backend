# InvoiceGen Email Service

A comprehensive, high-level email service built on top of the Mailtrap SDK, designed specifically for the InvoiceGen application.

## Features

✅ **Easy Integration** - Simple, intuitive API for sending emails  
✅ **Template Support** - Built-in HTML templates for common email types  
✅ **Attachment Handling** - Support for PDF invoices, quotes, and other files  
✅ **Sandbox/Production** - Easy switching between testing and live environments  
✅ **Bulk Email** - Efficient bulk email sending capabilities  
✅ **Error Handling** - Robust error handling and retry logic  
✅ **Configuration Management** - Environment-based configuration  
✅ **Email Categories** - Organized email types for tracking and analytics  

## Quick Start

### 1. Install Dependencies

The Mailtrap library is already installed via `uv`. If you need to install it manually:

```bash
pip install mailtrap
```

### 2. Configure Environment Variables

Add these to your `.env` file:

```env
# Required
MAILTRAP_API_KEY=your_api_token_here
MAILTRAP_USE_SANDBOX=true
MAILTRAP_INBOX_ID=your_inbox_id_here

# Optional
DEFAULT_SENDER_EMAIL=noreply@invoicegen.com
DEFAULT_SENDER_NAME=InvoiceGen
```

Get your API key from: https://mailtrap.io/api-tokens

### 3. Basic Usage

```python
from app.services import EmailService, EmailMessage, EmailAddress

# Create email service
email_service = EmailService()

# Send a simple email
message = EmailMessage(
    sender=EmailAddress(email="noreply@invoicegen.com", name="InvoiceGen"),
    to=[EmailAddress(email="client@example.com", name="John Doe")],
    subject="Welcome to InvoiceGen!",
    text="Thank you for joining us!",
    html="<h1>Welcome!</h1><p>Thank you for joining us!</p>"
)

response = email_service.send_email(message)
print(f"Email sent: {response}")
```

## Email Types & Convenience Methods

The service includes pre-built methods for common email scenarios:

### Welcome Email
```python
email_service.send_welcome_email(
    to_email="user@example.com",
    to_name="John Doe"
)
```

### Invoice Email with PDF
```python
email_service.send_invoice_email(
    to_email="client@example.com",
    to_name="Jane Smith",
    invoice_number="INV-001",
    invoice_pdf=pdf_bytes
)
```

### Quote Email with PDF
```python
email_service.send_quote_email(
    to_email="prospect@example.com",
    to_name="Bob Johnson",
    quote_number="QUO-001",
    quote_pdf=pdf_bytes
)
```

### Payment Reminder
```python
email_service.send_payment_reminder(
    to_email="client@example.com",
    to_name="John Doe",
    invoice_number="INV-001",
    amount_due="$1,500.00",
    due_date="2024-01-15"
)
```

### Password Reset
```python
email_service.send_password_reset_email(
    to_email="user@example.com",
    to_name="John Doe",
    reset_token="abc123",
    reset_url="https://invoicegen.com/reset?token=abc123"
)
```

### Email Verification
```python
email_service.send_verification_email(
    to_email="newuser@example.com",
    to_name="Jane Smith",
    verification_token="verify123",
    verification_url="https://invoicegen.com/verify?token=verify123"
)
```

## Advanced Usage

### Email with Attachments
```python
from app.services import EmailAttachment

# Create attachment
attachment = EmailAttachment(
    content=pdf_bytes,
    filename="invoice.pdf",
    mimetype="application/pdf"
)

# Send email with attachment
message = EmailMessage(
    sender=EmailAddress(email="invoices@invoicegen.com", name="InvoiceGen"),
    to=[EmailAddress(email="client@example.com", name="Client")],
    subject="Your Invoice",
    text="Please find your invoice attached.",
    attachments=[attachment]
)

email_service.send_email(message)
```

### Bulk Email Sending
```python
from app.services import create_email_service

# Create bulk email service
bulk_service = create_email_service(bulk_mode=True)

# Prepare multiple messages
messages = [
    EmailMessage(...),
    EmailMessage(...),
    EmailMessage(...)
]

# Send all at once
responses = bulk_service.send_bulk_emails(messages)
```

### Template-based Emails
```python
from app.services import EmailTemplate

template = EmailTemplate(
    template_uuid="your-template-uuid",
    template_variables={
        "user_name": "John Doe",
        "invoice_number": "INV-001"
    }
)

email_service.send_template_email(
    sender=EmailAddress(email="noreply@invoicegen.com", name="InvoiceGen"),
    to=[EmailAddress(email="client@example.com", name="John Doe")],
    template=template
)
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MAILTRAP_API_KEY` | Yes | - | Your Mailtrap API token |
| `MAILTRAP_USE_SANDBOX` | No | `true` | Use sandbox mode for testing |
| `MAILTRAP_INBOX_ID` | Yes* | - | Inbox ID (required for sandbox) |
| `MAILTRAP_BULK_MODE` | No | `false` | Enable bulk email mode |
| `DEFAULT_SENDER_EMAIL` | No | `noreply@invoicegen.com` | Default sender email |
| `DEFAULT_SENDER_NAME` | No | `InvoiceGen` | Default sender name |
| `EMAIL_ENVIRONMENT` | No | `development` | Environment (dev/staging/prod) |

*Required when `MAILTRAP_USE_SANDBOX=true`

### Sender Configuration

Different email types use different sender addresses:

- **Default**: `noreply@invoicegen.com`
- **Invoices**: `invoices@invoicegen.com`
- **Quotes**: `quotes@invoicegen.com`
- **Reminders**: `reminders@invoicegen.com`
- **Security**: `security@invoicegen.com`
- **Support**: `support@invoicegen.com`

### Environment Setup

Use the interactive setup script:

```bash
python app/services/email_config.py
```

Or manually configure your `.env` file using `.env.example` as a template.

## Testing

### Run Tests
```bash
python test_email_service.py
```

### Run Examples
```bash
python app/services/email_examples.py
```

### Configuration Validation
```python
from app.services.email_config import EmailConfigManager

config_manager = EmailConfigManager()
validation = config_manager.validate_configuration()
print(validation)
```

## Email Categories

The service supports categorized emails for better tracking:

- `TRANSACTIONAL` - System emails, confirmations
- `MARKETING` - Newsletters, promotions
- `NOTIFICATION` - Alerts, updates
- `INVOICE` - Invoice-related emails
- `QUOTE` - Quote-related emails
- `REMINDER` - Payment reminders
- `WELCOME` - Welcome emails
- `PASSWORD_RESET` - Password reset emails
- `VERIFICATION` - Email verification

## Error Handling

The service includes comprehensive error handling:

```python
try:
    response = email_service.send_email(message)
    print(f"Success: {response}")
except Exception as e:
    print(f"Email failed: {e}")
    # Handle error (retry, log, notify admin, etc.)
```

## Production Deployment

### 1. Update Environment
```env
MAILTRAP_USE_SANDBOX=false
EMAIL_ENVIRONMENT=production
```

### 2. Configure Domain
Update sender email addresses to use your domain:
```env
DEFAULT_SENDER_EMAIL=noreply@yourdomain.com
INVOICE_SENDER_EMAIL=invoices@yourdomain.com
```

### 3. Set Up SPF/DKIM
Configure your domain's DNS records for email authentication.

### 4. Monitor Usage
Use Mailtrap's analytics to monitor email delivery and performance.

## Integration Examples

### FastAPI Integration
```python
from fastapi import FastAPI, BackgroundTasks
from app.services import EmailService

app = FastAPI()
email_service = EmailService()

@app.post("/send-welcome-email")
async def send_welcome(email: str, name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        email_service.send_welcome_email,
        to_email=email,
        to_name=name
    )
    return {"message": "Welcome email queued"}
```

### GraphQL Integration
```python
import strawberry
from app.services import EmailService

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def send_invoice_email(self, invoice_id: str) -> bool:
        # Get invoice data
        invoice = get_invoice(invoice_id)
        pdf_bytes = generate_invoice_pdf(invoice)
        
        # Send email
        email_service = EmailService()
        email_service.send_invoice_email(
            to_email=invoice.client.email,
            to_name=invoice.client.name,
            invoice_number=invoice.number,
            invoice_pdf=pdf_bytes
        )
        return True
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ValueError: MAILTRAP_API_KEY environment variable or api_token parameter is required
   ```
   **Solution**: Set your Mailtrap API key in `.env`

2. **Inbox ID Missing**
   ```
   ValueError: inbox_id is required when use_sandbox is True
   ```
   **Solution**: Set `MAILTRAP_INBOX_ID` for sandbox mode

3. **SSL/Connection Issues**
   **Solution**: Check your network connection and API key validity

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Validate Configuration
```bash
python -c "from app.services.email_config import EmailConfigManager; print(EmailConfigManager().validate_configuration())"
```

## Support

- **Mailtrap Documentation**: https://help.mailtrap.io/
- **API Reference**: https://api-docs.mailtrap.io/
- **Python SDK**: https://github.com/railsware/mailtrap-python

## License

This email service is part of the InvoiceGen application and follows the same license terms.