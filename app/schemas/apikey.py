from pydantic import BaseModel
from datetime import datetime

class APIKeyCreate(BaseModel):
    key: str

class APIKeyRead(BaseModel):
    id: int
    key: str
    name: str
    created: datetime

    class Config:
        orm_mode = True
