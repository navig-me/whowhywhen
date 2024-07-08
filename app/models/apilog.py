from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class APILog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_project_id: int = Field(foreign_key="userproject.id")
    endpoint: str    
    bot_id: Optional[int] = Field(foreign_key="botinfo.id")
    ip_address: str
    request_info: str
    location: Optional[str] = None    
    response_code: Optional[int] = Field(default=None)
    response_time: Optional[float] = Field(default=None)
    created: datetime = Field(default_factory=datetime.now)
    user_project: "UserProject" = Relationship(back_populates="api_logs")
    botinfo: "BotInfo" = Relationship(back_populates="api_logs")
    created_at: datetime = Field(default_factory=datetime.now)
