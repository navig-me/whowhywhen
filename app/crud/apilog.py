from sqlmodel import Session, select
from app.models.apilog import APILog
from app.schemas.apilog import APILogCreate
from app.crud.user import increment_request_count, User
from datetime import datetime, timedelta
from sqlalchemy import select, func, extract, case

def create_apilog(db: Session, user_project_id: int, apilog: APILogCreate):
    db_apilog = APILog(user_project_id=user_project_id, **apilog.dict())
    db.add(db_apilog)
    db.commit()
    db.refresh(db_apilog)
    return db_apilog

def get_apilogs(db: Session, user_id: int, page: int = 1, limit: int = 10, project_id: int = None, search_params = None):
    offset = (page - 1) * limit
    
    if project_id:
        query = select(APILog).where(APILog.user_project_id == project_id)
    else:
        query = select(APILog).where(APILog.user_id == user_id)

    if search_params:
        if search_params.endpoint:
            query = query.where(APILog.endpoint.ilike(f'{search_params.endpoint}%'))
        if search_params.ip_address:
            query = query.where(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.request_info:
            query = query.where(APILog.request_info.ilike(f'{search_params.request_info}%'))
        if search_params.location:
            query = query.where(APILog.location.ilike(f'{search_params.location}%'))
        if search_params.response_code:
            query = query.where(APILog.response_code == search_params.response_code)
    
    query = query.offset(offset).limit(limit).order_by(APILog.created_at.desc())
    
    results = db.execute(query).scalars().all()
    total = db.query(APILog).filter(APILog.user_project_id == project_id if project_id else APILog.user_id == user_id).count()
    
    return {"logs": results, "total": total}


def get_apilogs_stats(db: Session, user_id: int, project_id: int = None, search_params = None, frequency: str = "hour"):
    end_date = datetime.now()

    if frequency == "minute":
        start_date = end_date - timedelta(hours=1)
        period_fmt = '%Y-%m-%d %H:%M'
        date_trunc = func.date_trunc('minute', APILog.created_at)
    elif frequency == "day":
        start_date = end_date - timedelta(days=30)
        period_fmt = '%Y-%m-%d'
        date_trunc = func.date_trunc('day', APILog.created_at)
    else:  # Default to hourly data
        start_date = end_date - timedelta(hours=24)
        period_fmt = '%Y-%m-%d %H'
        date_trunc = func.date_trunc('hour', APILog.created_at)

    query = db.query(APILog)
    if project_id:
        query = query.filter(APILog.user_project_id == project_id)
    else:
        query = query.filter(APILog.user_id == user_id)

    query = query.filter(APILog.created_at >= start_date).filter(APILog.created_at <= end_date)

    if search_params:
        if search_params.endpoint:
            query = query.filter(APILog.endpoint.ilike(f'{search_params.endpoint}%'))
        if search_params.ip_address:
            query = query.filter(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.request_info:
            query = query.filter(APILog.request_info.ilike(f'{search_params.request_info}%'))
        if search_params.location:
            query = query.filter(APILog.location.ilike(f'{search_params.location}%'))
        if search_params.response_code:
            query = query.filter(APILog.response_code == search_params.response_code)

    stats_query = (
        query.with_entities(
            date_trunc.label('period'),
            func.count(case((APILog.response_code.between(200, 299), 1), else_=None)).label('success_count'),
            func.count(case((APILog.response_code < 200, 1), (APILog.response_code >= 300, 1), else_=None)).label('error_count'),
            func.coalesce(func.avg(APILog.response_time), 0).label('avg_response_time')
        )
        .group_by(date_trunc)
        .order_by(date_trunc)
    )
    
    results = stats_query.all()
    
    full_periods = []
    current_period = start_date
    while current_period <= end_date:
        full_periods.append(current_period.strftime(period_fmt))
        if frequency == "minute":
            current_period += timedelta(minutes=1)
        elif frequency == "day":
            current_period += timedelta(days=1)
        else:
            current_period += timedelta(hours=1)
    
    counts = {result[0].strftime(period_fmt): {"success_count": result[1], "error_count": result[2], "avg_response_time": result[3]} for result in results}
    full_results = [{"period": period, "success_count": counts.get(period, {}).get("success_count", 0), "error_count": counts.get(period, {}).get("error_count", 0), "avg_response_time": counts.get(period, {}).get("avg_response_time", 0)} for period in full_periods]
    
    return full_results
