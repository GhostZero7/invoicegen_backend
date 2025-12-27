import strawberry
from typing import Optional
from sqlalchemy.orm import Session
from app.graphql.types.user import (
    User,
    CreateUserInput,
    UpdateUserInput,
    UpdatePasswordInput,
)
from app.db.models.user import User as UserModel
from app.auth.utils import hash_password, verify_password
from app.graphql.queries.user import user_model_to_type
import pyotp
import uuid
from app.services import EmailService
from app.core.config import settings

otp = pyotp.TOTP(settings.PYTOTP_SECRET_KEY)


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, info: strawberry.Info, input: CreateUserInput) -> User:
        """Create a new user"""
        db: Session = info.context["db"]
        
        # Check if user already exists
        existing_user = db.query(UserModel).filter(UserModel.email == input.email).first()
        if existing_user:
            raise Exception("User with this email already exists")
        
        # Create new user
        user = UserModel(
            id=str(uuid.uuid4()),
            email=input.email,
            password_hash=hash_password(input.password),
            first_name=input.first_name,
            last_name=input.last_name,
            phone=input.phone,
            role=input.role.value if input.role else "user",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        email_service = EmailService(api_token=settings.MAILTRAP_API_KEY, inbox_id=settings.MAILTRAP_INBOX_ID)
        email_service.send_verification_email(user.email, f'${user.first_name} {user.last_name}', otp.now(),otp.now() )
        
        return user_model_to_type(user)
    
    @strawberry.mutation
    def update_user(
        self,
        info: strawberry.Info,
        id: strawberry.ID,
        input: UpdateUserInput,
    ) -> User:
        """Update user information"""
        db: Session = info.context["db"]
        
        user = db.query(UserModel).filter(UserModel.id == str(id)).first()
        if not user:
            raise Exception("User not found")
        
        # Update fields if provided
        if input.first_name is not None:
            user.first_name = input.first_name
        if input.last_name is not None:
            user.last_name = input.last_name
        if input.phone is not None:
            user.phone = input.phone
        if input.avatar_url is not None:
            user.avatar_url = input.avatar_url
        if input.role is not None:
            user.role = input.role.value
        if input.status is not None:
            user.status = input.status.value
        
        db.commit()
        db.refresh(user)
        
        return user_model_to_type(user)
    
    @strawberry.mutation
    def update_password(self, info: strawberry.Info, input: UpdatePasswordInput) -> bool:
        """Update user password"""
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            raise Exception("Not authenticated")
        
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        if not user:
            raise Exception("User not found")
        
        # Verify current password
        if not verify_password(input.current_password, user.password_hash):
            raise Exception("Current password is incorrect")
        
        # Update password
        user.password_hash = hash_password(input.new_password)
        db.commit()
        
        return True
    
    @strawberry.mutation
    def delete_user(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a user (soft delete by setting status to DELETED)"""
        db: Session = info.context["db"]
        
        user = db.query(UserModel).filter(UserModel.id == str(id)).first()
        if not user:
            raise Exception("User not found")
        
        user.status = "deleted"
        db.commit()
        
        return True
    
    @strawberry.mutation
    def enable_two_factor(self, info: strawberry.Info) -> str:
        """Enable two-factor authentication and return secret"""
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            raise Exception("Not authenticated")
        
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        if not user:
            raise Exception("User not found")
        
        # Generate TOTP secret
        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        user.two_factor_enabled = True
        db.commit()
        
        return secret
    
    @strawberry.mutation
    def disable_two_factor(self, info: strawberry.Info, code: str) -> bool:
        """Disable two-factor authentication"""
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            raise Exception("Not authenticated")
        
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        if not user:
            raise Exception("User not found")
        
        if not user.two_factor_enabled:
            raise Exception("Two-factor authentication is not enabled")
        
        # Verify TOTP code
        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(code):
            raise Exception("Invalid verification code")
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        db.commit()
        
        return True
