import strawberry
from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import uuid
from app.graphql.types.category import Category, CreateCategoryInput, UpdateCategoryInput
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
        category_type=category_model.category_type,
        is_active=category_model.is_active,
        sort_order=category_model.sort_order,
        created_at=category_model.created_at,
        updated_at=category_model.updated_at,
        subcategories=None,  # Avoid recursion - load separately if needed
        parent=None,  # Avoid recursion - load separately if needed
    )

@strawberry.type
class CategoryMutation:
    @strawberry.mutation
    async def create_category(self, info: strawberry.Info, input: CreateCategoryInput) -> Category:
        """Create a new category"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Verify user owns the business
        business = db.query(BusinessProfile).filter(
            BusinessProfile.id == str(input.business_id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not business:
            raise Exception("Business not found")
        
        # Validate parent category if provided
        if input.parent_id:
            parent_category = db.query(CategoryModel).filter(
                CategoryModel.id == str(input.parent_id),
                CategoryModel.business_id == str(input.business_id)
            ).first()
            
            if not parent_category:
                raise Exception("Parent category not found")
            
            # Ensure parent and child have same category type
            if parent_category.category_type != input.category_type.value:
                raise Exception("Parent and child categories must have the same type")
        
        # Check if category name is unique within the business and type
        existing_category = db.query(CategoryModel).filter(
            CategoryModel.name == input.name,
            CategoryModel.business_id == str(input.business_id),
            CategoryModel.category_type == input.category_type.value,
            CategoryModel.parent_id == (str(input.parent_id) if input.parent_id else None)
        ).first()
        
        if existing_category:
            raise Exception("Category with this name already exists in this context")
        
        # Create the category
        category = CategoryModel(
            id=str(uuid.uuid4()),
            business_id=str(input.business_id),
            name=input.name,
            description=input.description,
            color=input.color,
            icon=input.icon,
            parent_id=str(input.parent_id) if input.parent_id else None,
            category_type=input.category_type.value,
            is_active=True,
            sort_order=input.sort_order,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(category)
        db.commit()
        db.refresh(category)
        
        return category_model_to_type(category)
    
    @strawberry.mutation
    async def update_category(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdateCategoryInput
    ) -> Category:
        """Update an existing category"""
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
            raise Exception("Category not found")
        
        # Validate parent category if being updated
        if input.parent_id and input.parent_id != category.parent_id:
            # Prevent circular references
            if str(input.parent_id) == category.id:
                raise Exception("Category cannot be its own parent")
            
            # Check if the new parent would create a circular reference
            def check_circular_reference(parent_id: str, target_id: str) -> bool:
                parent = db.query(CategoryModel).filter(CategoryModel.id == parent_id).first()
                if not parent:
                    return False
                if parent.parent_id == target_id:
                    return True
                if parent.parent_id:
                    return check_circular_reference(parent.parent_id, target_id)
                return False
            
            if check_circular_reference(str(input.parent_id), category.id):
                raise Exception("This would create a circular reference")
            
            parent_category = db.query(CategoryModel).filter(
                CategoryModel.id == str(input.parent_id),
                CategoryModel.business_id == category.business_id
            ).first()
            
            if not parent_category:
                raise Exception("Parent category not found")
            
            # Ensure parent and child have same category type
            if parent_category.category_type != category.category_type:
                raise Exception("Parent and child categories must have the same type")
        
        # Check name uniqueness if name is being updated
        if input.name and input.name != category.name:
            existing_category = db.query(CategoryModel).filter(
                CategoryModel.name == input.name,
                CategoryModel.business_id == category.business_id,
                CategoryModel.category_type == category.category_type,
                CategoryModel.parent_id == (str(input.parent_id) if input.parent_id else category.parent_id),
                CategoryModel.id != str(id)
            ).first()
            
            if existing_category:
                raise Exception("Category with this name already exists in this context")
        
        # Update fields
        if input.name is not None:
            category.name = input.name
        if input.description is not None:
            category.description = input.description
        if input.color is not None:
            category.color = input.color
        if input.icon is not None:
            category.icon = input.icon
        if input.parent_id is not None:
            category.parent_id = str(input.parent_id) if input.parent_id else None
        if input.is_active is not None:
            category.is_active = input.is_active
        if input.sort_order is not None:
            category.sort_order = input.sort_order
        
        category.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(category)
        
        return category_model_to_type(category)
    
    @strawberry.mutation
    async def delete_category(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a category (soft delete by setting is_active to False)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        # Get category and verify user owns the business
        category = db.query(CategoryModel).join(BusinessProfile).filter(
            CategoryModel.id == str(id),
            BusinessProfile.user_id == user.id
        ).first()
        
        if not category:
            raise Exception("Category not found")
        
        # Check if category has subcategories
        subcategories_count = db.query(CategoryModel).filter(
            CategoryModel.parent_id == str(id),
            CategoryModel.is_active == True
        ).count()
        
        if subcategories_count > 0:
            raise Exception("Cannot delete category with active subcategories")
        
        # Check if category is being used by invoices or expenses
        from app.db.models.invoice import Invoice
        from app.db.models.expense import Expense
        
        invoices_count = db.query(Invoice).filter(Invoice.category_id == str(id)).count()
        expenses_count = db.query(Expense).filter(Expense.category_id == str(id)).count()
        
        if invoices_count > 0 or expenses_count > 0:
            # Soft delete if category is in use
            category.is_active = False
            category.updated_at = datetime.utcnow()
            db.commit()
        else:
            # Hard delete if not in use
            db.delete(category)
            db.commit()
        
        return True
    
    @strawberry.mutation
    async def reorder_categories(
        self, 
        info: strawberry.Info, 
        category_ids: List[strawberry.ID]
    ) -> List[Category]:
        """Reorder categories by updating their sort_order"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        if not user:
            raise Exception("Not authenticated")
        
        categories = []
        
        for index, category_id in enumerate(category_ids):
            # Get category and verify user owns the business
            category = db.query(CategoryModel).join(BusinessProfile).filter(
                CategoryModel.id == str(category_id),
                BusinessProfile.user_id == user.id
            ).first()
            
            if not category:
                raise Exception(f"Category {category_id} not found")
            
            category.sort_order = index
            category.updated_at = datetime.utcnow()
            categories.append(category)
        
        db.commit()
        
        # Refresh all categories
        for category in categories:
            db.refresh(category)
        
        return [category_model_to_type(category) for category in categories]