import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import uuid
from app.graphql.types.waitlist import Waitlist, CreateWaitlistInput, UpdateWaitlistInput
from app.db.models.waitlist import Waitlist as WaitlistModel

def waitlist_model_to_type(waitlist_model: WaitlistModel) -> Waitlist:
    """Convert SQLAlchemy Waitlist model to Strawberry Waitlist type"""
    from app.graphql.types.waitlist import WaitlistPriority
    
    return Waitlist(
        id=strawberry.ID(waitlist_model.id),
        email=waitlist_model.email,
        first_name=waitlist_model.first_name,
        last_name=waitlist_model.last_name,
        company_name=waitlist_model.company_name,
        phone=waitlist_model.phone,
        message=waitlist_model.message,
        source=waitlist_model.source,
        utm_source=waitlist_model.utm_source,
        utm_medium=waitlist_model.utm_medium,
        utm_campaign=waitlist_model.utm_campaign,
        is_notified=waitlist_model.is_notified,
        is_converted=waitlist_model.is_converted,
        user_id=strawberry.ID(waitlist_model.user_id) if waitlist_model.user_id else None,
        priority=WaitlistPriority(waitlist_model.priority),
        tags=waitlist_model.tags,
        notes=waitlist_model.notes,
        ip_address=waitlist_model.ip_address,
        user_agent=waitlist_model.user_agent,
        created_at=waitlist_model.created_at,
        updated_at=waitlist_model.updated_at,
        notified_at=waitlist_model.notified_at,
        converted_at=waitlist_model.converted_at,
    )

@strawberry.type
class WaitlistMutation:
    @strawberry.mutation
    async def join_waitlist(self, info: strawberry.Info, input: CreateWaitlistInput) -> Waitlist:
        """Join the waitlist (Public endpoint)"""
        db: Session = info.context["db"]
        request = info.context.get("request")
        
        # Normalize email
        email = input.email.lower().strip()
        
        # Check if email already exists
        existing_entry = db.query(WaitlistModel).filter(
            WaitlistModel.email == email
        ).first()
        
        if existing_entry:
            # Return existing entry instead of creating duplicate
            return waitlist_model_to_type(existing_entry)
        
        # Get IP address and user agent from request
        ip_address = None
        user_agent = None
        if request:
            ip_address = request.client.host if hasattr(request, 'client') else None
            user_agent = request.headers.get("user-agent")
        
        # Create new waitlist entry
        waitlist_entry = WaitlistModel(
            id=str(uuid.uuid4()),
            email=email,
            first_name=input.first_name,
            last_name=input.last_name,
            company_name=input.company_name,
            phone=input.phone,
            message=input.message,
            source=input.source,
            utm_source=input.utm_source,
            utm_medium=input.utm_medium,
            utm_campaign=input.utm_campaign,
            priority=input.priority.value if input.priority else "normal",
            tags=input.tags,
            ip_address=ip_address,
            user_agent=user_agent,
            is_notified=False,
            is_converted=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(waitlist_entry)
        db.commit()
        db.refresh(waitlist_entry)
        
        return waitlist_model_to_type(waitlist_entry)
    
    @strawberry.mutation
    async def update_waitlist_entry(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID, 
        input: UpdateWaitlistInput
    ) -> Waitlist:
        """Update a waitlist entry (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can update waitlist entries
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        waitlist_entry = db.query(WaitlistModel).options(
            joinedload(WaitlistModel.user)
        ).filter(WaitlistModel.id == str(id)).first()
        
        if not waitlist_entry:
            raise Exception("Waitlist entry not found")
        
        # Update fields
        if input.first_name is not None:
            waitlist_entry.first_name = input.first_name
        if input.last_name is not None:
            waitlist_entry.last_name = input.last_name
        if input.company_name is not None:
            waitlist_entry.company_name = input.company_name
        if input.phone is not None:
            waitlist_entry.phone = input.phone
        if input.message is not None:
            waitlist_entry.message = input.message
        if input.source is not None:
            waitlist_entry.source = input.source
        if input.priority is not None:
            waitlist_entry.priority = input.priority.value
        if input.tags is not None:
            waitlist_entry.tags = input.tags
        if input.notes is not None:
            waitlist_entry.notes = input.notes
        if input.is_notified is not None:
            waitlist_entry.is_notified = input.is_notified
            if input.is_notified and not waitlist_entry.notified_at:
                waitlist_entry.notified_at = datetime.utcnow()
        if input.is_converted is not None:
            waitlist_entry.is_converted = input.is_converted
            if input.is_converted and not waitlist_entry.converted_at:
                waitlist_entry.converted_at = datetime.utcnow()
        if input.user_id is not None:
            waitlist_entry.user_id = str(input.user_id) if input.user_id else None
        
        waitlist_entry.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(waitlist_entry)
        
        return waitlist_model_to_type(waitlist_entry)
    
    @strawberry.mutation
    async def delete_waitlist_entry(self, info: strawberry.Info, id: strawberry.ID) -> bool:
        """Delete a waitlist entry (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can delete waitlist entries
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        waitlist_entry = db.query(WaitlistModel).filter(
            WaitlistModel.id == str(id)
        ).first()
        
        if not waitlist_entry:
            raise Exception("Waitlist entry not found")
        
        db.delete(waitlist_entry)
        db.commit()
        
        return True
    
    @strawberry.mutation
    async def mark_waitlist_notified(
        self, 
        info: strawberry.Info, 
        ids: List[strawberry.ID]
    ) -> List[Waitlist]:
        """Mark waitlist entries as notified (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can mark entries as notified
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        waitlist_entries = db.query(WaitlistModel).filter(
            WaitlistModel.id.in_([str(id) for id in ids])
        ).all()
        
        if not waitlist_entries:
            raise Exception("No waitlist entries found")
        
        updated_entries = []
        for entry in waitlist_entries:
            if not entry.is_notified:
                entry.is_notified = True
                entry.notified_at = datetime.utcnow()
                entry.updated_at = datetime.utcnow()
                updated_entries.append(entry)
        
        db.commit()
        
        # Refresh all entries
        for entry in updated_entries:
            db.refresh(entry)
        
        return [waitlist_model_to_type(entry) for entry in updated_entries]
    
    @strawberry.mutation
    async def mark_waitlist_converted(
        self, 
        info: strawberry.Info, 
        id: strawberry.ID,
        user_id: Optional[strawberry.ID] = None
    ) -> Waitlist:
        """Mark waitlist entry as converted to user (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can mark entries as converted
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        waitlist_entry = db.query(WaitlistModel).filter(
            WaitlistModel.id == str(id)
        ).first()
        
        if not waitlist_entry:
            raise Exception("Waitlist entry not found")
        
        waitlist_entry.is_converted = True
        waitlist_entry.converted_at = datetime.utcnow()
        waitlist_entry.updated_at = datetime.utcnow()
        
        if user_id:
            waitlist_entry.user_id = str(user_id)
        
        db.commit()
        db.refresh(waitlist_entry)
        
        return waitlist_model_to_type(waitlist_entry)
    
    @strawberry.mutation
    async def bulk_update_waitlist_priority(
        self, 
        info: strawberry.Info, 
        ids: List[strawberry.ID],
        priority: str
    ) -> List[Waitlist]:
        """Bulk update priority for waitlist entries (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can bulk update priorities
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        # Validate priority
        valid_priorities = ["normal", "high", "vip"]
        if priority not in valid_priorities:
            raise Exception(f"Invalid priority. Must be one of: {', '.join(valid_priorities)}")
        
        waitlist_entries = db.query(WaitlistModel).filter(
            WaitlistModel.id.in_([str(id) for id in ids])
        ).all()
        
        if not waitlist_entries:
            raise Exception("No waitlist entries found")
        
        for entry in waitlist_entries:
            entry.priority = priority
            entry.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Refresh all entries
        for entry in waitlist_entries:
            db.refresh(entry)
        
        return [waitlist_model_to_type(entry) for entry in waitlist_entries]