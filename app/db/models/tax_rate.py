from sqlalchemy import Column, String, Float, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class TaxRate(Base):
    __tablename__ = "tax_rates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    rate = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    tax_number = Column(String(50), nullable=True)
    is_compound = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="tax_rates")