from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import enum

class SubscriptionPlan(enum.Enum):
    free = "free"
    paid = "paid"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    domain: str
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)
    subscription_plan: SubscriptionPlan = Field(default=SubscriptionPlan.free)
    request_count: int = Field(default=0)
    last_request_reset: datetime = Field(default_factory=datetime.now)
    api_keys: List["APIKey"] = Relationship(back_populates="user")
