from sqlmodel import Session, select
from app.models.apilog import APILog
from app.schemas.apilog import APILogCreate
from app.crud.user import increment_request_count, User
from datetime import datetime, timedelta
from sqlalchemy import select, func, extract

def create_apilog(db: Session, user_project_id: int, apilog: APILogCreate):
    db_apilog = APILog(user_project_id=user_project_id, **apilog.dict())
    db.add(db_apilog)
    db.commit()
    db.refresh(db_apilog)
    return db_apilog

def get_apilogs(db: Session, user_id: int, page: int = 1, limit: int = 10, project_id: int = None):
    if project_id:
        return db.exec(select(APILog).where(APILog.user_project_id == project_id).offset((page - 1) * limit).limit(limit).order_by(APILog.created_at.desc()).all())
    else:
        return db.exec(select(APILog).where(APILog.user_id == user_id).offset((page - 1) * limit).limit(limit).order_by(APILog.created_at.desc()).all())

def get_apilogs_stats(db: Session, user_id: int, project_id: int = None):
    # Set start_date to 24 hours ago and end_date to now
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)
    
    # Base query
    query = db.query(APILog)
    if project_id:
        query = query.filter(APILog.user_project_id == project_id)
    else:
        query = query.filter(APILog.user_id == user_id)
    
    query = query.filter(APILog.created_at >= start_date).filter(APILog.created_at <= end_date)
    
    date_trunc = func.date_trunc('hour', APILog.created_at)

    stats_query = (
        query.with_entities(
            date_trunc.label('hour'),
            func.count(APILog.id).label('count')
        )
        .group_by(date_trunc)
        .order_by(date_trunc)
    )
    
    results = stats_query.all()
    return [{"hour": result[0], "count": result[1]} for result in results]
