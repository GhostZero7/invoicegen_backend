from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class AddressType(str, enum.Enum):
    BILLING = "billing"
    SHIPPING = "shipping"
    BUSINESS = "business"
    HOME = "home"

class Address(Base):
    __tablename__ = "addresses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    addressable_type = Column(String(50), nullable=False)  # 'user', 'business_profile', 'client'
    addressable_id = Column(String, nullable=False)
    address_type = Column(Enum(AddressType), nullable=False)
    street_line_1 = Column(String(255), nullable=False)
    street_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(2), nullable=False)  # ISO 3166-1 alpha-2
    is_default = Column(Boolean, default=False)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Polymorphic relationships - no back_populates since we're using generic foreign keys