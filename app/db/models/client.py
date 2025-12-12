from sqlalchemy import Column, String, Enum, Float, Text, ForeignKey, JSON, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class ClientType(str, enum.Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

class ClientStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    client_type = Column(Enum(ClientType), default=ClientType.INDIVIDUAL)
    company_name = Column(String(255), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    mobile = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)
    vat_number = Column(String(50), nullable=True)
    payment_terms = Column(String(20), nullable=True)  # References PaymentTerms enum
    credit_limit = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    language = Column(String(5), default="en")
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # For PostgreSQL use JSON, for MySQL use JSON type
    status = Column(Enum(ClientStatus), default=ClientStatus.ACTIVE, index=True)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="clients")
    contacts = relationship("ClientContact", back_populates="client", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="client")
    expenses = relationship("Expense", back_populates="client")
    quotes = relationship("Quote", back_populates="client")

class ClientContact(Base):
    __tablename__ = "client_contacts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    position = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="contacts")