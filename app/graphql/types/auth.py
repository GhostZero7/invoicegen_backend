import strawberry
from datetime import datetime
from typing import Optional, Dict
from enum import Enum
from app.graphql.types.user import User

@strawberry.type
class Auth:
    token: str = None
    user: Optional[User] = None
    is_verified: bool = False
    message: str = None

@strawberry.input
class LoginUserInput:
    email: str
    password: str
    remember: Optional[bool] = None

@strawberry.type
class VerificationEmail:
    email: str
    message: str

@strawberry.input
class ForgotPasswordInput:
    email: str

@strawberry.type
class ForgotPassword:
    message: str