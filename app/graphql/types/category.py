import strawberry
from datetime import datetime
from typing import Optional, List
from enum import Enum

@strawberry.enum
class CategoryType(Enum):
    INVOICE = "invoice"
    PRODUCT = "product"
    EXPENSE = "expense"

@strawberry.type
class Category:
    id: strawberry.ID
    business_id: strawberry.ID
    name: str
    description: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    parent_id: Optional[strawberry.ID]
    category_type: CategoryType
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    subcategories: Optional[List["Category"]] = None
    parent: Optional["Category"] = None

@strawberry.input
class CreateCategoryInput:
    business_id: strawberry.ID
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[strawberry.ID] = None
    category_type: CategoryType
    sort_order: int = 0

@strawberry.input
class UpdateCategoryInput:
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[strawberry.ID] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

@strawberry.input
class CategoryFilterInput:
    business_id: Optional[strawberry.ID] = None
    category_type: Optional[CategoryType] = None
    parent_id: Optional[strawberry.ID] = None
    is_active: Optional[bool] = None
    name: Optional[str] = None