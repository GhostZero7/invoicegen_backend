from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.models.user import User
from app.db.models.business import BusinessProfile
from app.business.schemas import BusinessProfileResponse, BusinessProfileCreate, BusinessProfileUpdate
from app.core.deps import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[BusinessProfileResponse])
async def get_business_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all business profiles for the current user"""
    business_profiles = db.query(BusinessProfile).filter(
        BusinessProfile.user_id == current_user.id
    ).all()
    
    return business_profiles

@router.get("/{business_id}", response_model=BusinessProfileResponse)
async def get_business_profile(
    business_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific business profile"""
    business = db.query(BusinessProfile).filter(
        BusinessProfile.id == business_id,
        BusinessProfile.user_id == current_user.id
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    return business

@router.post("/", response_model=BusinessProfileResponse)
async def create_business_profile(
    business_data: BusinessProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new business profile"""
    import uuid
    
    business = BusinessProfile(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        **business_data.dict()
    )
    
    db.add(business)
    db.commit()
    db.refresh(business)
    
    return business

@router.put("/{business_id}", response_model=BusinessProfileResponse)
async def update_business_profile(
    business_id: str,
    business_data: BusinessProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a business profile"""
    business = db.query(BusinessProfile).filter(
        BusinessProfile.id == business_id,
        BusinessProfile.user_id == current_user.id
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    # Update fields
    for field, value in business_data.dict(exclude_unset=True).items():
        setattr(business, field, value)
    
    db.commit()
    db.refresh(business)
    
    return business

@router.delete("/{business_id}")
async def delete_business_profile(
    business_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a business profile"""
    business = db.query(BusinessProfile).filter(
        BusinessProfile.id == business_id,
        BusinessProfile.user_id == current_user.id
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business profile not found"
        )
    
    db.delete(business)
    db.commit()
    
    return {"message": "Business profile deleted successfully"}