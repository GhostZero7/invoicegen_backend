from sqlalchemy import Column, String, Float, ForeignKey, Date, Enum, Text, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CHECK = "check"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    OTHER = "other"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=False, index=True)
    payment_number = Column(String(50), nullable=False, unique=True, index=True)
    payment_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    transaction_id = Column(String(255), nullable=True)
    reference_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.COMPLETED, index=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    creator = relationship("User", foreign_keys=[created_by])