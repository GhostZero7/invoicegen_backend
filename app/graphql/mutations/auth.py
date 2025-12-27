import strawberry
from app.graphql.types.auth import (
    Auth,
    LoginUserInput,
    VerificationEmail,
    ForgotPassword,
    ForgotPasswordInput
)

from app.db.models.user import User as UserModel,UserStatus
from sqlalchemy.orm import Session
from app.auth.utils import verify_password
from app.auth.utils import create_access_token
from fastapi import HTTPException, status
from app.services import EmailService
from app.core.config import settings
import pyotp


otp = pyotp.TOTP(settings.PYTOTP_SECRET_KEY, digits=6, interval=120)

@strawberry.type
class AuthMutation:

    @strawberry.mutation
    def login(self, info: strawberry.Info, input: LoginUserInput) -> Auth:
        
        if not input.email and not input.password:
            raise Exception("Not validate input")
        
        db: Session = info.context["db"]
        
        user = db.query(UserModel).filter_by(email=input.email).first()

        if not user:
            raise Exception("You do not have account with this email.")


        if user and verify_password(input.password, user.password_hash):
            if not user.email_verified:
                email_service = EmailService(api_token=settings.MAILTRAP_API_KEY, inbox_id=settings.MAILTRAP_INBOX_ID)
                email_service.send_verification_email(user.email, f'${user.first_name} {user.last_name}', otp.now(),otp.now() )
            
                return Auth(
                    message="Your account is not verified, We have sent a verification email",
                    token="",
                    is_verified=user.email_verified
                )
            if user.status != UserStatus.ACTIVE:
                raise Exception("Account is not active")
            
            print(user)

            token = create_access_token(data={"sub": user.email, "id": user.id})
            
            return Auth(
                token=token,
                user=user,
                message=f"You are now logged in. Welcome back {user.last_name}!",
                is_verified=user.email_verified
            )
            
        elif user and not verify_password(input.password):
            raise Exception("Password not match")
        else:
            raise Exception("User not found")

    @strawberry.mutation
    def verify_email(self, info: strawberry.Info, email: str, otp_: str) -> bool:
        """Verify user email with token"""
        print(email, otp_)
        
        # TODO: Implement token verification logic
        # This is a placeholder implementation
        if not email and not otp:
            raise Exception("Not validate input")
        
        db: Session = info.context["db"]
        
        user = db.query(UserModel).filter_by(email=email).first()
        if not otp_:
            raise Exception("Invalid OTP")

        if not otp.verify(otp_):
            raise Exception("The OTP has expired")
        
        user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if not user:
            raise Exception("User not found")
        
        user.email_verified = True
        db.commit()
        
        return True
    
    @strawberry.mutation
    def sendOTP(self, info: strawberry.Info, email:str) -> Auth:
        if not email and not otp:
            raise Exception("Not validate input")
        
        db: Session = info.context["db"]
        
        user = db.query(UserModel).filter_by(email=email).first()

        user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if not user:
            raise Exception("User not found")

        if not user.email_verified:
            email_service = EmailService(api_token=settings.MAILTRAP_API_KEY, inbox_id=settings.MAILTRAP_INBOX_ID)
            email_service.send_verification_email(user.email, f'${user.first_name} {user.last_name}', otp.now(),otp.now() )
        
            return Auth(
                message="We have sent a verification code to your email",
                token="",
                is_verified=False
            )
        raise Exception("Your account is already verified")
        
    @strawberry.mutation
    def forgot_password(self, info: strawberry.Info, input: ForgotPasswordInput)-> ForgotPassword:
        pass