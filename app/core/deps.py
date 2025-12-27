from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models.user import User
from redis import asyncio as aioredis


security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user

def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_optional),
    db: Session = Depends(get_db)
) -> User | None:
    """Optional authentication - returns None if not authenticated"""
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except (JWTError, AttributeError):
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.status != "active":
        return None
    return user

def get_redis_client(request: Request) -> aioredis.Redis:
    """Provides the Redis client instance stored in the app state."""
    # We access the redis client attached to the application state
    redis = request.app.state.redis
    if redis is None:
        raise HTTPException(status_code=500, detail="Redis service unavailable")
    return redis