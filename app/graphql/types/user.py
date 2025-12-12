import strawberry
from datetime import datetime
from typing import Optional
from enum import Enum

@strawberry.enum
class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"
    ACCOUNTANT = "accountant"

@strawberry.enum
class UserStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

@strawberry.type
class User:
    id: strawberry.ID
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    email_verified: bool
    two_factor_enabled: bool
    role: UserRole
    status: UserStatus
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

@strawberry.input
class CreateUserInput:
    email: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER

@strawberry.input
class UpdateUserInput:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None

@strawberry.input
class UpdatePasswordInput:
    current_password: str
    new_password: str

@strawberry.type
class AuthPayload:
    user: User
    access_token: str
    refresh_token: str
