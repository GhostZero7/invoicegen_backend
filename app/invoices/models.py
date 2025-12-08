from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
