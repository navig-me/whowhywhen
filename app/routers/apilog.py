from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.crud.apilog import create_apilog
from app.schemas.apilog import APILogCreate
from app.dependencies.apikey import get_api_key
from app.models.user import User

router = APIRouter()

@router.post("/log")
def save_api_log(apilog: APILogCreate, current_user: User = Depends(get_api_key), session: Session = Depends(get_session)):
    return create_apilog(session, current_user.id, apilog)
