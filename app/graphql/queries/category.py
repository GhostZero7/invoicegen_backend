import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.graphql.types.category import Category, CategoryFilterInput, CategoryType
from app.db.models.categories import Category as CategoryModel
from app.db.models.business import BusinessProfile

def category_model_to_type(category_model: CategoryModel) -> Category:
    """Convert SQLAlchemy Category model to Strawberry Category type"""
    return Category(
        id=strawberry.ID(category_model.id),
        business_id=strawberry.ID(category_model.business_id),
        name=category_model.name,
        description=category_model.description,
        color=category_model.color,
        icon=category_model.icon,
        parent_id=strawberry.ID(category_model.parent_id) if category_model.parent_id else None,
        category_type=CategoryType(category_model.category_type.value),
        is_active=category_model.is_active,
        sort_order=category_model.sort_order,
        created_at=category_model.created_at,
        updated_at=category_model.updated_at,
        subcategories=None,  # Avoid recursion - load separately if needed
        parent=None,  # Avoid recursion - load separately if needed
    )

@strawberry.type
class CategoryQuery:
    @strawberry.field
    def category(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Category]:
        """Get category by ID"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get category and verify user owns the business
        category = db.query(CategoryModel).options(
            joinedload(CategoryModel.parent),
            joinedload(CategoryModel.subcategories)
        ).join(BusinessProfile).filter(
            CategoryModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not category:
            return None
        
        return category_model_to_type(category)
    
    @strawberry.field
    def categories(
        self,
        info: strawberry.Info,
        filter: Optional[CategoryFilterInput] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Category]:
        """Get list of categories with optional filters"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Base query - only categories from user's businesses
        query = db.query(CategoryModel).options(
            joinedload(CategoryModel.parent),
            joinedload(CategoryModel.subcategories)
        ).join(BusinessProfile).filter(
            BusinessProfile.user_id == user.id
        )
        
        # Apply filters
        if filter:
            if filter.business_id:
                query = query.filter(CategoryModel.business_id == str(filter.business_id))
            
            if filter.category_type:
                query = query.filter(CategoryModel.category_type == filter.category_type.value)
            
            if filter.parent_id:
                query = query.filter(CategoryModel.parent_id == str(filter.parent_id))
            elif filter.parent_id is None:  # Explicitly filter for root categories
                query = query.filter(CategoryModel.parent_id.is_(None))
            
            if filter.is_active is not None:
                query = query.filter(CategoryModel.is_active == filter.is_active)
            
            if filter.name:
                query = query.filter(CategoryModel.name.ilike(f"%{filter.name}%"))
        
        # Order by sort_order and name, apply pagination
        categories = query.order_by(CategoryModel.sort_order, CategoryModel.name).offset(skip).limit(limit).all()
        
        return [category_model_to_type(category) for category in categories]
    
    @strawberry.field
    def categories_by_business(
        self,
        info: strawberry.Info,
        business_id: strawberry.ID,
        category_type: Optional[CategoryType] = None,
        active_only: bool = True,
        root_only: bool = False,
    ) -> List[Category]:
        """Get categories for a specific business"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business
        business = db.query(BusinessProfile).filter(
            BusinessProfile.id == str(business_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        query = db.query(CategoryModel).options(
            joinedload(CategoryModel.parent),
            joinedload(CategoryModel.subcategories)
        ).filter(
            CategoryModel.business_id == str(business_id)
        )
        
        if category_type:
            query = query.filter(CategoryModel.category_type == category_type.value)
        
        if active_only:
            query = query.filter(CategoryModel.is_active == True)
        
        if root_only:
            query = query.filter(CategoryModel.parent_id.is_(None))
        
        categories = query.order_by(CategoryModel.sort_order, CategoryModel.name).all()
        
        return [category_model_to_type(category) for category in categories]
    
    @strawberry.field
    def category_tree(
        self,
        info: strawberry.Info,
        business_id: strawberry.ID,
        category_type: Optional[CategoryType] = None,
    ) -> List[Category]:
        """Get hierarchical category tree for a business"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business
        business = db.query(BusinessProfile).filter(
            BusinessProfile.id == str(business_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        # Get only root categories (no parent)
        query = db.query(CategoryModel).options(
            joinedload(CategoryModel.subcategories)
        ).filter(
            CategoryModel.business_id == str(business_id),
            CategoryModel.parent_id.is_(None),
            CategoryModel.is_active == True
        )
        
        if category_type:
            query = query.filter(CategoryModel.category_type == category_type.value)
        
        root_categories = query.order_by(CategoryModel.sort_order, CategoryModel.name).all()
        
        return [category_model_to_type(category) for category in root_categories]