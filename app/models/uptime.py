from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import enum
import uuid

class MonitorType(enum.Enum):
    http = "http"
    https = "https"
    ping = "ping"

class MonitorStatus(enum.Enum):
    up = "up"
    down = "down"
    unknown = "unknown"

class UptimeMonitor(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    url: str = Field(index=True)
    type: MonitorType = Field(default=MonitorType.http)
    status: MonitorStatus = Field(default=MonitorStatus.unknown)
    check_interval: int = Field(default=5)  # in minutes
    payload: Optional[str] = None
    expected_response: Optional[str] = None
    is_public: bool = Field(default=False)  # Field to indicate if the monitor is public
    public_url: Optional[str] = None  # Field to store the public URL if monitor is public
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    project_id: uuid.UUID = Field(foreign_key="userproject.id")
    project: "UserProject" = Relationship(back_populates="monitors")
    status_history: List["UptimeMonitorStatus"] = Relationship(back_populates="monitor")
    alerts: List["Alert"] = Relationship(back_populates="monitor")
    task_id: Optional[uuid.UUID] = Field(default=None)

class UptimeMonitorStatus(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    monitor_id: uuid.UUID = Field(foreign_key="uptimemonitor.id")
    monitor: "UptimeMonitor" = Relationship(back_populates="status_history")
    status: "MonitorStatus" = Field(default=MonitorStatus.unknown)
    response_time: Optional[float] = Field(default=None)
    response_code: Optional[int] = Field(default=None)
    response_code_text: Optional[str] = Field(default=None)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)

class AlertType(enum.Enum):
    email = "email"
    sms = "sms"
    webhook = "webhook"

class Alert(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    monitor_id: uuid.UUID = Field(foreign_key="uptimemonitor.id")
    monitor: "UptimeMonitor" = Relationship(back_populates="alerts")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="alerts")
    type: AlertType = Field(default=AlertType.email)
    threshold: int = Field(default=1)  # number of failures before alerting
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    status_history: List["AlertStatus"] = Relationship(back_populates="alert")

class AlertStatus(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    alert_id: uuid.UUID = Field(foreign_key="alert.id")
    alert: "Alert" = Relationship(back_populates="status_history")
    status: MonitorStatus = Field(default=MonitorStatus.unknown)
    response_time: Optional[float] = Field(default=None)
    response_code: Optional[int] = Field(default=None)
    response_code_text: Optional[str] = Field(default=None)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
