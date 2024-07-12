from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr
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
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    project_id: uuid.UUID = Field(foreign_key="userproject.id")
    project: "UserProject" = Relationship(back_populates="monitors")

class UptimeMonitorStatus(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    monitor_id: uuid.UUID = Field(foreign_key="uptimemonitor.id")
    status: MonitorStatus = Field(default=MonitorStatus.unknown)
    response_time: Optional[float] = Field(default=None)
    response_code: Optional[int] = Field(default=None)
    response_code_text: Optional[str] = Field(default=None)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
