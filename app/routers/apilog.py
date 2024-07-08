from fastapi import APIRouter, Depends
from typing import Optional, List
from typing import Optional
from sqlmodel import Session
from app.database import get_session
from app.crud.apilog import create_apilog, get_apilogs, get_apilogs_stats, create_apilog_bulk
from app.schemas.apilog import APILogCreate, APILogSearch
from app.dependencies.apikey import get_api_key
from app.dependencies.auth import get_current_user
from app.models.user import UserProject, User

router = APIRouter()

@router.post("/log")
async def save_api_log(apilog: APILogCreate, current_user_project: UserProject = Depends(get_api_key), session: Session = Depends(get_session)):
    return await create_apilog(session, current_user_project.id, apilog)

@router.post("/log/bulk")
async def save_api_log_bulk(apilogs: List[APILogCreate], current_user_project: UserProject = Depends(get_api_key), session: Session = Depends(get_session)):
    return await create_apilog_bulk(session, current_user_project.id, apilogs)

@router.post("/logs/project/{project_id}")
def get_api_logs(
    project_id: int,
    search_params: Optional[APILogSearch] = None,
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_apilogs(session, current_user.id, page, limit, project_id, search_params)


@router.post("/logs/project/stats/{project_id}")
def get_api_logs_stats(
    project_id: int,
    search_params: Optional[APILogSearch] = None,
    frequency: str = "hour",
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_apilogs_stats(session, current_user.id, project_id, search_params, frequency)
