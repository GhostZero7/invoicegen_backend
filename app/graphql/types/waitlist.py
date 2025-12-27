import strawberry
from datetime import datetime
from typing import Optional
from enum import Enum

@strawberry.enum
class WaitlistPriority(Enum):
    NORMAL = "normal"
    HIGH = "high"
    VIP = "vip"

@strawberry.type
class Waitlist:
    id: strawberry.ID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    phone: Optional[str]
    message: Optional[str]
    source: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    is_notified: bool
    is_converted: bool
    user_id: Optional[strawberry.ID]
    priority: WaitlistPriority
    tags: Optional[str]
    notes: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime
    updated_at: datetime
    notified_at: Optional[datetime]
    converted_at: Optional[datetime]

@strawberry.input
class CreateWaitlistInput:
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    priority: Optional[WaitlistPriority] = WaitlistPriority.NORMAL
    tags: Optional[str] = None

@strawberry.input
class UpdateWaitlistInput:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None
    priority: Optional[WaitlistPriority] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    is_notified: Optional[bool] = None
    is_converted: Optional[bool] = None
    user_id: Optional[strawberry.ID] = None

@strawberry.input
class WaitlistFilterInput:
    email: Optional[str] = None
    company_name: Optional[str] = None
    source: Optional[str] = None
    priority: Optional[WaitlistPriority] = None
    is_notified: Optional[bool] = None
    is_converted: Optional[bool] = None
    tags: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

@strawberry.type
class WaitlistStats:
    total_count: int
    notified_count: int
    converted_count: int
    conversion_rate: float
    recent_signups: int  # Last 7 days