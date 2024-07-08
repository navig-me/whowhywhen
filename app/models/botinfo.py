from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid


class BotType(str, Enum):
    search_engine = "search_engine"
    social_media = "social_media"
    ai = "ai"
    seo = "seo"
    chatbot = "chatbot"

class BotInfo(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    bot_name: str = Field(index=True)
    website: Optional[str] = Field(default=None)
    bot_type: BotType = Field(default=BotType.search_engine)
    bot_details: Optional[str]
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    api_logs: List["APILog"] = Relationship(back_populates="botinfo")
