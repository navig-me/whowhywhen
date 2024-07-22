from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import SubscriptionPlan
import uuid

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    project_name: str
    cf_turnstile_response: str

class ChangePasswordForm(BaseModel):
    old_password: str
    new_password: str

class UserProjectRead(BaseModel):
    id: uuid.UUID
    project_name: str
    created: datetime
    modified: datetime
    active: bool


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    created: datetime
    modified: datetime
    active: bool
    monthly_credit_limit: int
    monthly_credit_usage_crossed: bool
    monthly_credit_limit_reset: datetime
    subscription_plan: Optional[SubscriptionPlan]
    two_factor_enabled: bool

class UserStatusRead(BaseModel):
    user_request_count: int
    user: UserRead

