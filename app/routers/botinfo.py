from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.crud.botinfo import create_botinfo
from app.schemas.botinfo import BotInfoCreate

router = APIRouter()

@router.post("/bots")
def save_bot_information(botinfo: BotInfoCreate, session: Session = Depends(get_session)):
    return create_botinfo(session, botinfo)
