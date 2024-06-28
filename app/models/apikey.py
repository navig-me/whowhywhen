from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    user_project_id: int = Field(foreign_key="userproject.id")
    created: datetime = Field(default_factory=datetime.now)
    name: str = Field(default="")
    user_project: "UserProject" = Relationship(back_populates="api_keys")
