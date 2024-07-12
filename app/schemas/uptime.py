from pydantic import BaseModel
from typing import Optional
from app.models.uptime import MonitorType


class MonitorCreate(BaseModel):
    name: str
    url: str
    type: MonitorType
    check_interval: int

class MonitorUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    type: Optional[MonitorType] = None
    check_interval: Optional[int] = None
