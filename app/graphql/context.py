from typing import Optional
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user_optional, get_current_user, get_redis_client
from app.db.models.user import User
from redis import asyncio as aioredis


async def get_context(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    redis_client: aioredis.Redis = Depends(get_redis_client)
):
    """Create GraphQL context with database session and current user"""
    # Debug logging
    auth_header = request.headers.get("authorization")
    print(f"🔍 Auth header: {auth_header[:50] if auth_header else 'None'}...")
    print(f"🔍 Current user: {current_user.email if current_user else 'None'}")
    
    return {
        "request": request,
        "db": db,
        "current_user": current_user,
        "redis": redis_client
    }

async def get_context_with_auth(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Required auth
    redis_client: aioredis.Redis = Depends(get_redis_client)
):
    """Create GraphQL context with required authentication"""
    return {
        "request": request,
        "db": db,
        "current_user": current_user,
        "redis": redis_client
    }
