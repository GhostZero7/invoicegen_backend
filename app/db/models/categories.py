from sqlalchemy import Column, String, Text, Enum, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid
from app.db.database import Base

class CategoryType(str, enum.Enum):
    INVOICE = "invoice"
    PRODUCT = "product"
    EXPENSE = "expense"

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # Hex color
    icon = Column(String(50), nullable=True)
    parent_id = Column(String, ForeignKey("categories.id"), nullable=True)
    category_type = Column(Enum(CategoryType), nullable=False)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    invoices = relationship("Invoice", back_populates="category")
    expenses = relationship("Expense", back_populates="category")