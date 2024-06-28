from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    domain: str

class UserRead(BaseModel):
    id: int
    email: str
    domain: str
    created: datetime
    modified: datetime
    active: bool

    class Config:
        orm_mode = True
