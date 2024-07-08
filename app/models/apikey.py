from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class APIKey(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    key: str = Field(index=True, unique=True)
    user_project_id: uuid.UUID = Field(foreign_key="userproject.id")
    created: datetime = Field(default_factory=datetime.now)
    name: str = Field(default="")
    user_project: "UserProject" = Relationship(back_populates="api_keys")
