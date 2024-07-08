from pydantic import BaseModel
from datetime import datetime
import uuid

class APIKeyCreate(BaseModel):
    key: str
    

class APIKeyRead(BaseModel):
    id: uuid.UUID
    key: str
    name: str
    created: datetime

    class Config:
        orm_mode = True
