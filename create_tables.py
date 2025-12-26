import sys
sys.path.append('.')

from app.db.database import Base, engine
from app.db.models.user import User
from app.db.models.business import BusinessProfile
from app.db.models.address import Address
from app.db.models.client import Client, ClientContact
from app.db.models.product import Product
from app.db.models.categories import Category
from app.db.models.qoute import Quote, QuoteItem
from app.db.models.payment import Payment
from app.db.models.invoice_reminder import InvoiceReminder
from app.db.models.expense import Expense
from app.db.models.tax_rate import TaxRate
from app.db.models.notification import Notification
from app.db.models.audit_log import AuditLog
from app.db.models.invoice import Invoice, InvoiceItem
from app.db.models.verification_code import VerificationCode

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")