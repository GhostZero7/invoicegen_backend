from typing import Optional
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user_optional
from app.db.models.user import User

async def get_context(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Create GraphQL context with database session and current user"""
    return {
        "request": request,
        "db": db,
        "current_user": current_user,
    }
