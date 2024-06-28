from sqlmodel import Session, select
from app.models.apilog import APILog
from app.schemas.apilog import APILogCreate
from app.crud.user import increment_request_count, User

def create_apilog(db: Session, user_project_id: int, apilog: APILogCreate):
    db_apilog = APILog(user_project_id=user_project_id, **apilog.dict())
    db.add(db_apilog)
    db.commit()
    db.refresh(db_apilog)
    return db_apilog

def get_apilogs(db: Session, user_id: int, page: int = 1, limit: int = 10):
    return db.exec(select(APILog).where(APILog.user_id == user_id).offset((page - 1) * limit).limit(limit).order_by(APILog.created_at.desc()).all())