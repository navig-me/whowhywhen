from fastapi import APIRouter, Depends
from typing import Optional, List
from typing import Optional
from sqlmodel import Session
from app.database import get_session
from app.crud.apilog import create_apilog, get_apilogs, get_apilogs_stats, create_apilog_bulk, get_counts_data, get_bot_logs_stats_data
from app.schemas.apilog import APILogCreate, APILogSearch
from app.dependencies.apikey import get_api_key
from app.dependencies.auth import get_current_user
from app.models.user import UserProject, User
from datetime import datetime, timedelta
import uuid

router_api = APIRouter()
router_dash = APIRouter()

@router_api.post("/log", summary="Save a single API log", description="Save a single API log entry.")
async def save_api_log(
    apilog: APILogCreate, 
    current_user_project: UserProject = Depends(get_api_key), 
    session: Session = Depends(get_session)
):
    """
    Save a single API log entry.

    - **url**: URL of the API request.
    - **ip_address**: IP address of the request.
    - **user_agent**: User agent of the request (optional).
    - **location**: Location of the request (optional).
    - **response_code**: HTTP response code (optional).
    - **response_time**: Response time in seconds (optional).
    """
    return await create_apilog(session, current_user_project.id, apilog)


@router_api.post("/log/bulk", summary="Save multiple API logs", description="Save multiple API log entries in bulk.")
async def save_api_log_bulk(
    apilogs: List[APILogCreate], 
    current_user_project: UserProject = Depends(get_api_key), 
    session: Session = Depends(get_session)
):
    """
    Save multiple API log entries in bulk.

    - **apilogs**: List of API log entries.
    """
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
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    bots_only: bool = False,  # Add this parameter
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_apilogs(session, current_user.id, page, limit, project_id, search_params, query, sort, sort_direction, start_datetime, end_datetime, bots_only)


@router_dash.post("/logs/project/stats/{project_id}")
def get_api_logs_stats(
    project_id: uuid.UUID,
    search_params: Optional[APILogSearch] = None,
    frequency: str = "hour",
    query: Optional[str] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    bots_only: bool = False,  # Add this parameter
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_apilogs_stats(session, current_user.id, project_id, search_params, frequency, query, start_datetime, end_datetime, bots_only)


@router_dash.post("/logs/project/device-stats/{project_id}")
def get_counts(
    project_id: uuid.UUID,
    search_params: Optional[APILogSearch] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    bots_only: bool = False,  # Add this parameter
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    counts_data = get_counts_data(session, current_user.id, project_id, search_params, start_datetime, end_datetime, bots_only)
    return {"counts": counts_data}


@router_dash.post("/logs/project/bot-stats/{project_id}")
def get_bot_logs_stats(
    project_id: uuid.UUID,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_bot_logs_stats_data(session, current_user.id, project_id, start_datetime, end_datetime)
