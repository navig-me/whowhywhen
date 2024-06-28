from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class APILog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    request_info: str
    is_bot: bool = Field(default=False)
    location: Optional[str] = None
    created: datetime = Field(default_factory=datetime.now)
