from pydantic import BaseModel
from datetime import datetime

class BotInfoCreate(BaseModel):
    bot_name: str
    bot_details: str

class BotInfoRead(BaseModel):
    id: int
    bot_name: str
    bot_details: str
    created: datetime

    class Config:
        orm_mode = True
