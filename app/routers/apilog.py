from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.crud.apilog import create_apilog, get_apilogs
from app.schemas.apilog import APILogCreate
from app.dependencies.apikey import get_api_key
from app.dependencies.auth import get_current_user
from app.models.user import UserProject, User

router = APIRouter()

@router.post("/log")
def save_api_log(apilog: APILogCreate, current_user_project: UserProject = Depends(get_api_key), session: Session = Depends(get_session)):
    return create_apilog(session, current_user_project.id, apilog)


@router.get("/logs")
def get_api_logs(current_user: User = Depends(get_current_user), page: int = 1, limit: int = 10, session: Session = Depends(get_session)):
    return get_apilogs(session, current_user.id, page, limit)
