import enum
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint



class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)
    projects: List["UserProject"] = Relationship(back_populates="user")
    totp_secret: Optional[str] = Field(default=None)
    two_factor_enabled: Optional[bool] = Field(default=False)


class UserProject(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)
    is_default: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="projects")
    api_keys: List["APIKey"] = Relationship(back_populates="user_project")
    api_logs: List["APILog"] = Relationship(back_populates="user_project")


class UserAlertConfig(SQLModel, table=True):
    __tablename__ = "useralertconfig"
    __table_args__ = (
        UniqueConstraint("user_project_id", name="unique_user_project_id"),
    )

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_project_id: uuid.UUID = Field(foreign_key="userproject.id")
    server_error_threshold: Optional[int] = Field(default=10)  # Number of 5xx errors
    client_error_threshold: Optional[int] = Field(default=20)  # Number of 4xx errors
    slow_threshold: Optional[int] = Field(
        default=1000
    )  # Slow response threshold in milliseconds
    slow_threshold_threshold: int = Field(default=10)  # Number of slow responses
    check_interval: int = Field(default=10)  # Interval to check for alerts
    last_checked: Optional[datetime] = Field(default=None)


class UserAlertNotificationEmail(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_project_id: uuid.UUID = Field(foreign_key="userproject.id")
    email_subject: str = Field(default="")
    email_body: str = Field(default="")
    created: datetime = Field(default_factory=datetime.now)


class UserAlertNotification(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_project_id: uuid.UUID = Field(foreign_key="userproject.id")
    user_alert_notification_email_id: Optional[uuid.UUID] = Field(
        foreign_key="useralertnotificationemail.id", default=None
    )
    description: str = Field(default="")

    server_error_threshold: Optional[int] = Field(default=None)
    server_error_threshold_actual: Optional[int] = Field(default=None)

    client_error_threshold: Optional[int] = Field(default=None)
    client_error_threshold_actual: Optional[int] = Field(default=None)

    slow_threshold: Optional[int] = Field(default=None)
    slow_threshold_threshold: Optional[int] = Field(default=None)
    slow_threshold_threshold_actual: Optional[int] = Field(default=None)

    check_interval: Optional[int] = Field(default=None)

    created: datetime = Field(default_factory=datetime.now)
    read_at: Optional[datetime] = Field(default=None)


class UserPushSubscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    endpoint: str
    p256dh: str
    auth: str
