import strawberry
from app.graphql.types.auth import (
    Auth,
    LoginUserInput
)

from app.db.models.user import User as UserModel,UserStatus
from sqlalchemy.orm import Session
from app.auth.utils import verify_password
from app.auth.utils import create_access_token
from fastapi import HTTPException, status
@strawberry.type
class AuthMutation:

    @strawberry.mutation
    def login(self, info: strawberry.Info, input: LoginUserInput) -> Auth:
        
        if not input.email and not input.password:
            raise Exception("Not validate input")
        
        db: Session = info.context["db"]
        
        user = db.query(UserModel).filter_by(email=input.email).first()

        if user and verify_password(input.password, user.password_hash):
            if user.status != UserStatus.ACTIVE:
                raise Exception("Account is not active")

            token = create_access_token(data={"sub": user.email, "id": user.id})
            
            return Auth(
                token=token,
                user=user
            )
            
        elif user and not verify_password(input.password):
            raise Exception("Password not match")
        else:
            raise Exception("User not found")



        