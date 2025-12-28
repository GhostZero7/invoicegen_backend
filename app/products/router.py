from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.product import Product
from app.db.models.business import BusinessProfile
from app.products.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.core.deps import get_db, get_current_user
from app.db.models.user import User

router = APIRouter(tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(BusinessProfile).filter(BusinessProfile.user_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")
    
    db_product = Product(**product_in.dict(), business_id=business.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(BusinessProfile).filter(BusinessProfile.user_id == current_user.id).first()
    if not business:
        return []
    
    return db.query(Product).filter(Product.business_id == business.id).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    business = db.query(BusinessProfile).filter(BusinessProfile.id == product.business_id).first()
    if not business or business.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this product")
        
    return product
