from sqlalchemy import Column, String, Boolean, Integer, Date, Enum, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class BusinessType(str, enum.Enum):
    SOLE_PROPRIETOR = "sole_proprietor"
    LLC = "llc"
    CORPORATION = "corporation"
    PARTNERSHIP = "partnership"

class PaymentTerms(str, enum.Enum):
    DUE_ON_RECEIPT = "due_on_receipt"
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_60 = "net_60"
    CUSTOM = "custom"

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    business_name = Column(String(255), nullable=False)
    business_type = Column(Enum(BusinessType), nullable=False)
    tax_id = Column(String(50), nullable=True, unique=True)
    vat_number = Column(String(50), nullable=True)
    registration_number = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=False)
    logo_url = Column(Text, nullable=True)
    currency = Column(String(3), default="USD")
    timezone = Column(String(50), default="UTC")
    fiscal_year_end = Column(Date, nullable=True)
    invoice_prefix = Column(String(10), default="INV")
    quote_prefix = Column(String(10), default="QUO")
    next_invoice_number = Column(Integer, default=1)
    next_quote_number = Column(Integer, default=1)
    payment_terms_default = Column(Enum(PaymentTerms), default=PaymentTerms.NET_30)
    notes_default = Column(Text, nullable=True)
    payment_instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="business_profiles")
    clients = relationship("Client", back_populates="business")
    invoices = relationship("Invoice", back_populates="business")
    products = relationship("Product", back_populates="business")
    categories = relationship("Category", back_populates="business")
    expenses = relationship("Expense", back_populates="business")
    tax_rates = relationship("TaxRate", back_populates="business")
    quotes = relationship("Quote", back_populates="business")
    