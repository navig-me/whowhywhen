import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


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
    bot_type: Optional[BotType] = Field(default=None, nullable=True)
    bot_details: Optional[str] = Field(default=None, nullable=True)
    pattern: Optional[str] = Field(default=None, nullable=True)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    api_logs: List["APILog"] = Relationship(back_populates="botinfo")
