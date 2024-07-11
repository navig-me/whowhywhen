from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime
import enum
import uuid

class SubscriptionPlan(enum.Enum):
    free = "free"
    starter = "starter"
    pro = "pro"

class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)
    subscription_plan: SubscriptionPlan = Field(default=SubscriptionPlan.free)
    monthly_credit_limit: int = Field(default=20000)
    monthly_credit_usage_crossed: bool = Field(default=False)
    monthly_credit_limit_reset: datetime = Field(default_factory=datetime.now)
    projects: List["UserProject"] = Relationship(back_populates="user")
    stripe_customer_id: Optional[str] = Field(default=None)

class UserProject(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)
    is_default: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="projects")
    api_keys: List["APIKey"] = Relationship(back_populates="user_project")
    api_logs: List["APILog"] = Relationship(back_populates="user_project")
