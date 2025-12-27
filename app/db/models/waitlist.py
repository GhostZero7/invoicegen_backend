from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class Waitlist(Base):
    __tablename__ = "waitlists"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    company_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    message = Column(Text, nullable=True)
    source = Column(String(50), nullable=True)  # Where they came from (website, referral, etc.)
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    is_notified = Column(Boolean, default=False)  # Whether they've been notified about launch
    is_converted = Column(Boolean, default=False)  # Whether they became a user
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)  # If they converted
    priority = Column(String(20), default="normal")  # normal, high, vip
    tags = Column(Text, nullable=True)  # Comma-separated tags
    notes = Column(Text, nullable=True)  # Internal notes
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    notified_at = Column(DateTime, nullable=True)
    converted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])