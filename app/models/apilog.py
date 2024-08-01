from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from typing import List

class APILog(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_project_id: Optional[uuid.UUID] = Field(foreign_key="userproject.id")
    url: str
    bot_id: Optional[uuid.UUID] = Field(foreign_key="botinfo.id")
    ip_address: str = Field(default="")
    location: Optional[str] = None    

    user_agent: str = Field(default="")
    user_agent_browser_family: Optional[str] = Field(default="")
    user_agent_browser_version: Optional[str] = Field(default="")
    user_agent_os_family: Optional[str] = Field(default="")
    user_agent_os_version: Optional[str] = Field(default="")
    user_agent_device_family: Optional[str] = Field(default="")
    user_agent_device_brand: Optional[str] = Field(default="")
    user_agent_device_model: Optional[str] = Field(default="")
    is_mobile: Optional[bool] = Field(default=None)
    is_tablet: Optional[bool] = Field(default=None)
    is_pc: Optional[bool] = Field(default=None)
    is_touch_capable: Optional[bool] = Field(default=None)
    is_bot: Optional[bool] = Field(default=None)
    
    response_code: Optional[int] = Field(default=None)
    response_code_text: Optional[str] = Field(default=None)
    response_time: Optional[float] = Field(default=None)
    
    path: Optional[str] = Field(default=None)
    query_params: List["APILogQueryParam"] = Relationship(back_populates="api_log")
    
    created: datetime = Field(default_factory=datetime.now)
    
    user_project: "UserProject" = Relationship(back_populates="api_logs")
    botinfo: "BotInfo" = Relationship(back_populates="api_logs")
    created_at: datetime = Field(default_factory=datetime.now)

class APILogQueryParam(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    api_log_id: uuid.UUID = Field(foreign_key="apilog.id")
    key: str
    value: str
    api_log: "APILog" = Relationship(back_populates="query_params")

class APILogNotification(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
