from sqlmodel import Session

from app.models.botinfo import BotInfo
from app.schemas.botinfo import BotInfoCreate


def create_botinfo(db: Session, botinfo: BotInfoCreate):
    db_botinfo = BotInfo(**botinfo.dict())
    db.add(db_botinfo)
    db.commit()
    db.refresh(db_botinfo)
    return db_botinfo
