from sqlalchemy import Column, String, Float, ForeignKey, Date, Enum, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True, index=True)
    vendor_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    expense_date = Column(Date, nullable=False, index=True)
    payment_method = Column(String(50), nullable=True)
    reference_number = Column(String(100), nullable=True)
    receipt_url = Column(Text, nullable=True)
    is_billable = Column(Boolean, default=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=True, index=True)
    notes = Column(Text, nullable=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    client = relationship("Client", back_populates="expenses")
    invoice = relationship("Invoice", foreign_keys=[invoice_id])
    creator = relationship("User", foreign_keys=[created_by])