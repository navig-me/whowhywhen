import uuid
from datetime import datetime

from pydantic import BaseModel


class APIKeyCreate(BaseModel):
    key: str
    

class APIKeyRead(BaseModel):
    id: uuid.UUID
    key: str
    name: str
    created: datetime

    class Config:
        orm_mode = True
