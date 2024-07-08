from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class APILogCreate(BaseModel):
    endpoint: str
    ip_address: str
    request_info: str
    location: Optional[str] = None
    response_code: Optional[int] = None
    response_time: Optional[float] = None
    created_at: Optional[datetime] = datetime.now()


class APILogSearch(BaseModel):
    endpoint: Optional[str] = None
    ip_address: Optional[str] = None
    request_info: Optional[str] = None
    location: Optional[str] = None
    response_code: Optional[int] = None


class APILogRead(BaseModel):
    id: int
    request_info: str
    is_bot: bool
    location: Optional[str]
    response_code: Optional[int] = None
    response_time: Optional[float] = None
    created: datetime

    class Config:
        orm_mode = True
