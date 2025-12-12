from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.user import User, UserStatus
from app.auth.schemas import UserCreate, UserLogin, Token
from app.auth.utils import hash_password, verify_password, create_access_token, generate_user_id

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    exists = db.query(User).filter(User.email == user_data.email).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        id=generate_user_id(),
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        email_verified=False,
        status=UserStatus.ACTIVE
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create token
    token = create_access_token({"sub": str(new_user.id), "email": new_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    
    if not db_user or not verify_password(user_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if db_user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )

    # Update last login
    db_user.last_login_at = datetime.utcnow()
    db.commit()

    token = create_access_token({"sub": str(db_user.id), "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}