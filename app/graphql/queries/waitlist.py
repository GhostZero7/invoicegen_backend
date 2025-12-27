import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.graphql.types.waitlist import Waitlist, WaitlistFilterInput, WaitlistStats, WaitlistPriority
from app.db.models.waitlist import Waitlist as WaitlistModel

def waitlist_model_to_type(waitlist_model: WaitlistModel) -> Waitlist:
    """Convert SQLAlchemy Waitlist model to Strawberry Waitlist type"""
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
class WaitlistQuery:
    @strawberry.field
    def waitlist_entry(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Waitlist]:
        """Get waitlist entry by ID (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can view waitlist entries
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        waitlist_entry = db.query(WaitlistModel).options(
            joinedload(WaitlistModel.user)
        ).filter(WaitlistModel.id == str(id)).first()
        
        if not waitlist_entry:
            return None
        
        return waitlist_model_to_type(waitlist_entry)
    
    @strawberry.field
    def waitlist_entries(
        self,
        info: strawberry.Info,
        filter: Optional[WaitlistFilterInput] = None,
        skip: int = 0,
        limit: int = 50,
        order_by: str = "created_at",
        order_desc: bool = True,
    ) -> List[Waitlist]:
        """Get list of waitlist entries with optional filters (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can view waitlist entries
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        query = db.query(WaitlistModel).options(
            joinedload(WaitlistModel.user)
        )
        
        # Apply filters
        if filter:
            if filter.email:
                query = query.filter(WaitlistModel.email.ilike(f"%{filter.email}%"))
            
            if filter.company_name:
                query = query.filter(WaitlistModel.company_name.ilike(f"%{filter.company_name}%"))
            
            if filter.source:
                query = query.filter(WaitlistModel.source == filter.source)
            
            if filter.priority:
                query = query.filter(WaitlistModel.priority == filter.priority.value)
            
            if filter.is_notified is not None:
                query = query.filter(WaitlistModel.is_notified == filter.is_notified)
            
            if filter.is_converted is not None:
                query = query.filter(WaitlistModel.is_converted == filter.is_converted)
            
            if filter.tags:
                query = query.filter(WaitlistModel.tags.ilike(f"%{filter.tags}%"))
            
            if filter.created_after:
                query = query.filter(WaitlistModel.created_at >= filter.created_after)
            
            if filter.created_before:
                query = query.filter(WaitlistModel.created_at <= filter.created_before)
        
        # Apply ordering
        if order_by == "created_at":
            order_column = WaitlistModel.created_at
        elif order_by == "email":
            order_column = WaitlistModel.email
        elif order_by == "company_name":
            order_column = WaitlistModel.company_name
        elif order_by == "priority":
            order_column = WaitlistModel.priority
        else:
            order_column = WaitlistModel.created_at
        
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        # Apply pagination
        waitlist_entries = query.offset(skip).limit(limit).all()
        
        return [waitlist_model_to_type(entry) for entry in waitlist_entries]
    
    @strawberry.field
    def waitlist_by_email(self, info: strawberry.Info, email: str) -> Optional[Waitlist]:
        """Get waitlist entry by email (Public - for checking if already signed up)"""
        db: Session = info.context["db"]
        
        waitlist_entry = db.query(WaitlistModel).filter(
            WaitlistModel.email == email.lower().strip()
        ).first()
        
        if not waitlist_entry:
            return None
        
        # Return limited info for public access
        return Waitlist(
            id=strawberry.ID(waitlist_entry.id),
            email=waitlist_entry.email,
            first_name=waitlist_entry.first_name,
            last_name=waitlist_entry.last_name,
            company_name=waitlist_entry.company_name,
            phone=None,  # Don't expose phone publicly
            message=None,  # Don't expose message publicly
            source=waitlist_entry.source,
            utm_source=None,  # Don't expose UTM data publicly
            utm_medium=None,
            utm_campaign=None,
            is_notified=waitlist_entry.is_notified,
            is_converted=waitlist_entry.is_converted,
            user_id=None,  # Don't expose user_id publicly
            priority=WaitlistPriority(waitlist_entry.priority),
            tags=None,  # Don't expose tags publicly
            notes=None,  # Don't expose notes publicly
            ip_address=None,  # Don't expose IP publicly
            user_agent=None,  # Don't expose user agent publicly
            created_at=waitlist_entry.created_at,
            updated_at=waitlist_entry.updated_at,
            notified_at=waitlist_entry.notified_at,
            converted_at=waitlist_entry.converted_at,
        )
    
    @strawberry.field
    def waitlist_stats(self, info: strawberry.Info) -> WaitlistStats:
        """Get waitlist statistics (Admin only)"""
        db: Session = info.context["db"]
        user = info.context.get("current_user")
        
        # Only admins can view waitlist stats
        if not user or user.role != "admin":
            raise Exception("Access denied. Admin privileges required.")
        
        # Get total count
        total_count = db.query(WaitlistModel).count()
        
        # Get notified count
        notified_count = db.query(WaitlistModel).filter(
            WaitlistModel.is_notified == True
        ).count()
        
        # Get converted count
        converted_count = db.query(WaitlistModel).filter(
            WaitlistModel.is_converted == True
        ).count()
        
        # Calculate conversion rate
        conversion_rate = (converted_count / total_count * 100) if total_count > 0 else 0.0
        
        # Get recent signups (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_signups = db.query(WaitlistModel).filter(
            WaitlistModel.created_at >= seven_days_ago
        ).count()
        
        return WaitlistStats(
            total_count=total_count,
            notified_count=notified_count,
            converted_count=converted_count,
            conversion_rate=round(conversion_rate, 2),
            recent_signups=recent_signups,
        )
    
    @strawberry.field
    def waitlist_position(self, info: strawberry.Info, email: str) -> Optional[int]:
        """Get position in waitlist by email (Public)"""
        db: Session = info.context["db"]
        
        waitlist_entry = db.query(WaitlistModel).filter(
            WaitlistModel.email == email.lower().strip()
        ).first()
        
        if not waitlist_entry:
            return None
        
        # Count entries created before this one
        position = db.query(WaitlistModel).filter(
            WaitlistModel.created_at < waitlist_entry.created_at
        ).count()
        
        return position + 1  # Position is 1-based