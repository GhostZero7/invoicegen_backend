from sqlalchemy import Column, String, Float, ForeignKey, Boolean, Date, Enum, Integer, Text, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentTerms(str, enum.Enum):
    DUE_ON_RECEIPT = "due_on_receipt"
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_60 = "net_60"
    CUSTOM = "custom"

class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class RecurringFrequency(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True, index=True)
    invoice_number = Column(String(50), nullable=False, index=True, unique=True)
    reference_number = Column(String(100), nullable=True)
    purchase_order_number = Column(String(100), nullable=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, index=True)
    invoice_date = Column(Date, nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)
    payment_terms = Column(Enum(PaymentTerms), nullable=False)
    custom_due_days = Column(Integer, nullable=True)
    subtotal = Column(Float, nullable=False, default=0.0)
    discount_type = Column(Enum(DiscountType), nullable=True)
    discount_value = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    amount_paid = Column(Float, default=0.0)
    amount_due = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), default="USD")
    exchange_rate = Column(Float, default=1.0000)
    notes = Column(Text, nullable=True)
    payment_instructions = Column(Text, nullable=True)
    footer_text = Column(Text, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_frequency = Column(Enum(RecurringFrequency), nullable=True)
    recurring_end_date = Column(Date, nullable=True)
    parent_invoice_id = Column(String, ForeignKey("invoices.id"), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    viewed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    pdf_url = Column(Text, nullable=True)
    public_url = Column(Text, nullable=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="invoices")
    client = relationship("Client", back_populates="invoices")
    category = relationship("Category", back_populates="invoices")
    creator = relationship("User", foreign_keys=[created_by])
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")
    reminders = relationship("InvoiceReminder", back_populates="invoice", cascade="all, delete-orphan")
    parent = relationship("Invoice", remote_side=[id], backref="child_invoices")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=True, index=True)
    description = Column(Text, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    unit_of_measure = Column(String(20), default="unit")
    tax_rate = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_type = Column(Enum(DiscountType), nullable=True)
    discount_value = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    line_total = Column(Float, nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")