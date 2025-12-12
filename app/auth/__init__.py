"""Authentication package.

Handles user authentication, JWT tokens, and authorization.
"""

from app.auth.router import router
from app.auth.utils import hash_password, verify_password, create_access_token
from app.auth.schemas import UserCreate, UserLogin, Token

__all__ = [
    "router",
    "hash_password",
    "verify_password",
    "create_access_token",
    "UserCreate",
    "UserLogin",
    "Token",
]