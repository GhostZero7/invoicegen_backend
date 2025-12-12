from sqlalchemy import Column, String, Float, ForeignKey, Boolean, Integer, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("business_profiles.id"), nullable=False, index=True)
    sku = Column(String(100), nullable=True, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    unit_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=True)
    unit_of_measure = Column(String(20), default="unit")
    tax_rate = Column(Float, default=0.0)
    is_taxable = Column(Boolean, default=True)
    track_inventory = Column(Boolean, default=False)
    quantity_in_stock = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, nullable=True)
    image_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business = relationship("BusinessProfile", back_populates="products")
    invoice_items = relationship("InvoiceItem", back_populates="product")