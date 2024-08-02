from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.user import create_user_alert_config, get_user_alert_configs
from app.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserAlertConfigCreate, UserAlertConfigRead
from app.services.monitoring_service import fetch_user_alert_configs

router = APIRouter()

@router.post("/alerts/config", response_model=UserAlertConfigRead)
def save_user_alert_config(
    alert_config: UserAlertConfigCreate, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    return create_user_alert_config(session, current_user.id, alert_config)

@router.get("/alerts", response_model=List[UserAlertConfigRead])
def get_user_alert_configs(
    current_user: User = Depends(get_current_user), 
    page: int = 1,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    configs_results, total = fetch_user_alert_configs(session, current_user.id, page, limit)
    return {
        "results": configs_results,
        "total": total
    }
