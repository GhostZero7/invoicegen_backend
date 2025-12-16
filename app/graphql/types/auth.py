import strawberry
from datetime import datetime
from typing import Optional, Dict
from enum import Enum
from app.graphql.types.user import User

@strawberry.type
class Auth:
    token: str
    user: Optional[User] = None

@strawberry.input
class LoginUserInput:
    email: str
    password: str
    remember: Optional[bool] = None