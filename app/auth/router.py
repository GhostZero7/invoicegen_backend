from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import SessionLocal
from app.db.models.user import User, UserStatus
from app.auth.schemas import UserCreate, UserLogin, Token, EmailVerificationRequest, VerifyOtpRequest
from app.auth.utils import hash_password, verify_password, create_access_token, generate_user_id

router = APIRouter(tags=["Auth"])

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
    
    # Return token and user data as a dictionary (FastAPI handles Pydantic conversion)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user
    }

@router.post("/request-verification")
def request_verification(
    request: EmailVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    import random
    from datetime import timedelta
    from app.db.models.verification_code import VerificationCode
    from app.utils.email import send_verification_email

    # ... existing code ...

    # Generate 6 digit code
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    expires = datetime.utcnow() + timedelta(minutes=10)

    # Check if a code entry exists
    try:
        db_code = db.query(VerificationCode).filter(VerificationCode.email == request.email).first()
        if db_code:
            db_code.code = code
            db_code.expires_at = expires
        else:
            db_code = VerificationCode(email=request.email, code=code, expires_at=expires)
            db.add(db_code)
        
        db.commit()

        # PRINT CODE to console for debugging/fallback
        print(f"\n\n==================================================")
        print(f"🔑 VERIFICATION CODE FOR {request.email}: {code}")
        print(f"==================================================\n\n")

        # FILE FALLBACK
        try:
            with open("otp_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.utcnow()}] Code for {request.email}: {code}\n")
        except Exception as fe:
            print(f"Failed to write to otp_log.txt: {fe}")

        # Send Email in Background
        background_tasks.add_task(send_verification_email, request.email, code)

        return {"message": "Verification code generated"}
    except Exception as e:
        print(f"ERROR in request_verification: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-email")
def verify_email(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    from app.db.models.verification_code import VerificationCode

    db_code = db.query(VerificationCode).filter(
        VerificationCode.email == request.email,
        VerificationCode.code == request.otp
    ).first()

    if not db_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )

    if db_code.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code expired"
        )
    
    # Optionally delete code after use or mark as used
    # db.delete(db_code)
    # db.commit()

    return {"message": "Email verified successfully"}
