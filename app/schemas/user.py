from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    project_name: str
    cf_turnstile_response: str

class UserProjectRead(BaseModel):
    id: int
    project_name: str
    created: datetime
    modified: datetime
    active: bool

class UserRead(BaseModel):
    id: int
    email: str
    created: datetime
    modified: datetime
    active: bool
