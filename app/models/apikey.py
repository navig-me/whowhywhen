from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.models.user import User

class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    user_id: int = Field(foreign_key="user.id")
    created: datetime = Field(default_factory=datetime.now)
    user: User = Relationship(back_populates="api_keys")
    name: str = Field(default="")
