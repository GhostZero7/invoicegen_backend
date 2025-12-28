from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime

class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str
    description: Optional[str] = None
    unit_price: float = Field(ge=0)
    cost_price: Optional[float] = Field(ge=0, default=None)
    unit_of_measure: str = "unit"
    tax_rate: float = Field(ge=0, default=0.0)
    is_taxable: bool = True
    track_inventory: bool = False
    quantity_in_stock: int = 0
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: str
    business_id: str
    product_name: str
    created_at: date
    updated_at: date

    @validator('product_name', pre=True, always=True)
    def set_product_name(cls, v, values):
        return v or values.get('name')

    class Config:
        from_attributes = True
