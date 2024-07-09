from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class APILog(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_project_id: uuid.UUID = Field(foreign_key="userproject.id")
    url: str
    bot_id: Optional[uuid.UUID] = Field(foreign_key="botinfo.id")
    ip_address: str
    user_agent: str
    location: Optional[str] = None    
    response_code: Optional[int] = Field(default=None)
    response_time: Optional[float] = Field(default=None)
    query_params: Optional[dict] = Field(default=None)
    path: Optional[str] = Field(default=None)
    
    created: datetime = Field(default_factory=datetime.now)
    
    user_project: "UserProject" = Relationship(back_populates="api_logs")
    botinfo: "BotInfo" = Relationship(back_populates="api_logs")
    created_at: datetime = Field(default_factory=datetime.now)
