from pydantic import BaseModel
from datetime import datetime
import uuid

class BotInfoCreate(BaseModel):
    bot_name: str
    bot_details: str

class BotInfoRead(BaseModel):
    id: uuid.UUID
    bot_name: str
    bot_details: str
    created: datetime

    class Config:
        orm_mode = True
