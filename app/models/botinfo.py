from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class BotInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bot_name: str
    bot_details: str
    created: datetime = Field(default_factory=datetime.now)
