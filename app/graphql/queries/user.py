import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.graphql.types.user import User, UserRole, UserStatus
from app.db.models.user import User as UserModel
from app.core.deps import get_current_user

def user_model_to_type(user_model: UserModel) -> User:
    """Convert SQLAlchemy User model to Strawberry User type"""
    return User(
        id=strawberry.ID(user_model.id),
        email=user_model.email,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        phone=user_model.phone,
        avatar_url=user_model.avatar_url,
        email_verified=user_model.email_verified,
        two_factor_enabled=user_model.two_factor_enabled,
        role=UserRole(user_model.role.value),
        status=UserStatus(user_model.status.value),
        last_login_at=user_model.last_login_at,
        created_at=user_model.created_at,
        updated_at=user_model.updated_at,
    )

@strawberry.type
class UserQuery:
    @strawberry.field
    def me(self, info: strawberry.Info) -> Optional[User]:
        """Get current authenticated user"""
        db: Session = info.context["db"]
        current_user = info.context.get("current_user")
        
        if not current_user:
            return None
        
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        if not user:
            return None
        
        return user_model_to_type(user)
    
    @strawberry.field
    def user(self, info: strawberry.Info, id: strawberry.ID) -> Optional[User]:
        """Get user by ID"""
        db: Session = info.context["db"]
        user = db.query(UserModel).filter(UserModel.id == str(id)).first()
        
        if not user:
            return None
        
        return user_model_to_type(user)
    
    @strawberry.field
    def users(
        self,
        info: strawberry.Info,
        skip: int = 0,
        limit: int = 10,
        role: Optional[UserRole] = None,
        status: Optional[UserStatus] = None,
    ) -> List[User]:
        """Get list of users with optional filters"""
        db: Session = info.context["db"]
        query = db.query(UserModel)
        
        if role:
            query = query.filter(UserModel.role == role.value)
        
        if status:
            query = query.filter(UserModel.status == status.value)
        
        users = query.offset(skip).limit(limit).all()
        
        return [user_model_to_type(user) for user in users]
