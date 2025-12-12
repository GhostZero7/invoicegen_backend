from sqlalchemy import Column, String, Float, ForeignKey, Date, Enum, Text, DateTime, Integer
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class QuoteStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CONVERTED = "converted"

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    quote_number = Column(String(50), nullable=False, index=True, unique=True)
    reference_number = Column(String(100), nullable=True)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.DRAFT, index=True)
    quote_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)
    discount_type = Column(String(20), nullable=True)  # 'percentage', 'fixed'
    discount_value = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), default="USD")
    notes = Column(Text, nullable=True)
    terms_conditions = Column(Text, nullable=True)
    converted_invoice_id = Column(String, ForeignKey("invoices.id"), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    viewed_at = Column(DateTime, nullable=True)
    accepted_at = Column(DateTime, nullable=True)
    declined_at = Column(DateTime, nullable=True)
    pdf_url = Column(Text, nullable=True)
    public_url = Column(Text, nullable=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="quotes")
    client = relationship("Client", back_populates="quotes")
    creator = relationship("User", foreign_keys=[created_by])
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    converted_invoice = relationship("Invoice", foreign_keys=[converted_invoice_id])

class QuoteItem(Base):
    __tablename__ = "quote_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quote_id = Column(String, ForeignKey("quotes.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=True, index=True)
    description = Column(Text, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    unit_of_measure = Column(String(20), default="unit")
    tax_rate = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    line_total = Column(Float, nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("Product")