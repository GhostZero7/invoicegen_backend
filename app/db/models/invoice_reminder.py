from sqlalchemy import Column, String, Integer, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class ReminderType(str, enum.Enum):
    BEFORE_DUE = "before_due"
    ON_DUE = "on_due"
    AFTER_DUE = "after_due"

class ReminderStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class InvoiceReminder(Base):
    __tablename__ = "invoice_reminders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=False, index=True)
    reminder_type = Column(Enum(ReminderType), nullable=False)
    days_offset = Column(Integer, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    status = Column(Enum(ReminderStatus), default=ReminderStatus.PENDING, index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="reminders")