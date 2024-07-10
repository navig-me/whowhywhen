from fastapi import APIRouter, Depends
from typing import Optional, List
from typing import Optional
from sqlmodel import Session
from app.database import get_session
from app.crud.apilog import create_apilog, get_apilogs, get_apilogs_stats, create_apilog_bulk, get_counts_data
from app.schemas.apilog import APILogCreate, APILogSearch
from app.dependencies.apikey import get_api_key
from app.dependencies.auth import get_current_user
from app.models.user import UserProject, User
import uuid

router_api = APIRouter()
router_dash = APIRouter()

@router_api.post("/log")
async def save_api_log(apilog: APILogCreate, current_user_project: UserProject = Depends(get_api_key), session: Session = Depends(get_session)):
    return await create_apilog(session, current_user_project.id, apilog)

@router_api.post("/log/bulk")
async def save_api_log_bulk(apilogs: List[APILogCreate], current_user_project: UserProject = Depends(get_api_key), session: Session = Depends(get_session)):
    return await create_apilog_bulk(session, current_user_project.id, apilogs)

@router_dash.post("/logs/project/{project_id}")
def get_api_logs(
    project_id: uuid.UUID,
    search_params: Optional[APILogSearch] = None,
    page: int = 1,
    limit: int = 10,
    query: Optional[str] = None,
    sort: Optional[str] = None,
    sort_direction: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_apilogs(session, current_user.id, page, limit, project_id, search_params, query, sort, sort_direction)


@router_dash.post("/logs/project/stats/{project_id}")
def get_api_logs_stats(
    project_id: uuid.UUID,
    search_params: Optional[APILogSearch] = None,
    frequency: str = "hour",
    query: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_apilogs_stats(session, current_user.id, project_id, search_params, frequency, query)


@router_dash.post("/logs/project/stats/{project_id}/counts")
def get_counts(
    project_id: uuid.UUID,
    search_params: Optional[APILogSearch] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_counts_data(session, current_user.id, project_id, search_params)

