from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.client import Client
from app.db.models.business import BusinessProfile
from app.clients.schemas import ClientCreate, ClientResponse, ClientUpdate
from app.core.deps import get_db, get_current_user
from app.db.models.user import User

router = APIRouter(tags=["Clients"])

@router.post("/", response_model=ClientResponse)
def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(BusinessProfile).filter(BusinessProfile.user_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")
    
    db_client = Client(**client_in.dict(), business_id=business.id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=List[ClientResponse])
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    business = db.query(BusinessProfile).filter(BusinessProfile.user_id == current_user.id).first()
    if not business:
        return []
    
    return db.query(Client).filter(Client.business_id == business.id).all()

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    business = db.query(BusinessProfile).filter(BusinessProfile.id == client.business_id).first()
    if not business or business.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this client")
        
    return client
