from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class APILogCreate(BaseModel):
    url: str
    ip_address: str
    user_agent: str
    location: Optional[str] = None
    response_code: Optional[int] = None
    response_time: Optional[float] = None
    created_at: Optional[datetime] = None


class APILogSearch(BaseModel):
    path: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None
    response_code: Optional[int] = None


class APILogRead(BaseModel):
    id: uuid.UUID
    user_agent: str
    is_bot: bool
    location: Optional[str]
    response_code: Optional[int] = None
    response_time: Optional[float] = None
    created: datetime

    class Config:
        orm_mode = True
