from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Date
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    ACCOUNTANT = "accountant"

class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(Text, nullable=True)
    email_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business_profiles = relationship("BusinessProfile", back_populates="owner", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user")
    invoices_created = relationship("Invoice", foreign_keys="Invoice.created_by", back_populates="creator")
    quotes_created = relationship("Quote", foreign_keys="Quote.created_by", back_populates="creator")
    payments_created = relationship("Payment", foreign_keys="Payment.created_by", back_populates="creator")
    expenses_created = relationship("Expense", foreign_keys="Expense.created_by", back_populates="creator")
    notifications = relationship("Notification", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    