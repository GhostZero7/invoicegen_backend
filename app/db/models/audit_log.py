from sqlalchemy import Column, String, Enum, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class AuditAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    entity_type = Column(String(50), nullable=False)  # Table name
    entity_id = Column(String, nullable=False)
    action = Column(Enum(AuditAction), nullable=False)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")