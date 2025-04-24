import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    project_name: Optional[str] = None


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
    two_factor_enabled: bool


class UserStatusRead(BaseModel):
    user_request_count: int
    unread_alert_count: int
    user: UserRead


class UserAlertConfigCreate(BaseModel):
    server_error_interval: Optional[int]
    server_error_threshold_minutes: int
    client_error_threshold: Optional[int]
    client_error_threshold_interval: int
    slow_threshold: Optional[int]
    slow_threshold_interval: int
    notification_interval: int


class UserAlertConfigRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    server_error_interval: Optional[int]
    server_error_threshold_minutes: int
    client_error_threshold: Optional[int]
    client_error_threshold_interval: int
    slow_threshold: Optional[int]
    slow_threshold_interval: int
    notification_interval: int
    created: datetime


class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscriptionCreate(BaseModel):
    endpoint: str
    keys: PushSubscriptionKeys
