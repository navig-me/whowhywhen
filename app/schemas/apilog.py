from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class APILogCreate(BaseModel):
    request_info: str
    is_bot: bool
    location: Optional[str]

class APILogRead(BaseModel):
    id: int
    request_info: str
    is_bot: bool
    location: Optional[str]
    created: datetime

    class Config:
        orm_mode = True
