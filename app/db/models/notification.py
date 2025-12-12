from sqlalchemy import Column, String, Enum, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class NotificationType(str, enum.Enum):
    INVOICE_PAID = "invoice_paid"
    INVOICE_OVERDUE = "invoice_overdue"
    QUOTE_ACCEPTED = "quote_accepted"
    QUOTE_DECLINED = "quote_declined"
    PAYMENT_RECEIVED = "payment_received"
    INVOICE_SENT = "invoice_sent"
    QUOTE_SENT = "quote_sent"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    related_type = Column(String(50), nullable=True)  # 'invoice', 'quote', 'payment', etc.
    related_id = Column(String, nullable=True)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="notifications")