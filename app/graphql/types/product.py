import strawberry
from datetime import date
from typing import Optional

@strawberry.type
class Product:
    id: strawberry.ID
    business_id: strawberry.ID
    sku: Optional[str]
    name: str
    description: Optional[str]
    unit_price: float
    cost_price: Optional[float]
    unit_of_measure: str
    tax_rate: float
    is_taxable: bool
    track_inventory: bool
    quantity_in_stock: int
    low_stock_threshold: Optional[int]
    image_url: Optional[str]
    is_active: bool
    created_at: date
    updated_at: date

@strawberry.input
class CreateProductInput:
    business_id: strawberry.ID
    sku: Optional[str] = None
    name: str = ""
    description: Optional[str] = None
    unit_price: float = 0.0
    cost_price: Optional[float] = None
    unit_of_measure: str = "unit"
    tax_rate: float = 0.0
    is_taxable: bool = True
    track_inventory: bool = False
    quantity_in_stock: int = 0
    low_stock_threshold: Optional[int] = None
    image_url: Optional[str] = None

@strawberry.input
class UpdateProductInput:
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    unit_of_measure: Optional[str] = None
    tax_rate: Optional[float] = None
    is_taxable: Optional[bool] = None
    track_inventory: Optional[bool] = None
    quantity_in_stock: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

@strawberry.input
class ProductFilterInput:
    business_id: Optional[strawberry.ID] = None
    name: Optional[str] = None
    sku: Optional[str] = None
    is_active: Optional[bool] = None
    track_inventory: Optional[bool] = None
    low_stock_only: Optional[bool] = None