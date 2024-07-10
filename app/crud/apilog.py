from sqlmodel import Session, select
from app.models.apilog import APILog, APILogQueryParam
from app.schemas.apilog import APILogCreate, APILogSearch
from app.crud.user import User
from datetime import datetime, timedelta
from sqlalchemy import select, func, extract, case
from typing import List, Optional
from sqlmodel import or_
import uuid
import httpx
import traceback
from urllib.parse import urlparse, parse_qs
from http.client import responses
from user_agents import parse
from sqlalchemy.sql import case

async def get_geolocation(ip: str):
    if ip and ',' in ip:
        ip = ip.split(',')[0]
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://ipinfo.io/{ip}/json?token=352e1fa66d5869')
        return response.json()

async def get_url_components(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # If no scheme is provided, assume 'https'
    if not parsed_url.scheme:
        url = 'https://' + url
        parsed_url = urlparse(url)

    # Extract the path
    path = parsed_url.path
    
    # Parse query parameters and keep only those with values
    raw_query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    query_params = {key: value[0] for key, value in raw_query_params.items() if value[0]}
    
    # Reconstruct the URL without query parameters
    full_url = f"{parsed_url.scheme}://{parsed_url.netloc}{path}"
    
    return full_url, path, query_params

def get_response_code_text(code: int):
    print("Getting response code text for", code)
    if code:
        return responses.get(code, None)
    return None

def parse_user_agent(apilog: APILog):
    print("Parsing user agent", apilog.user_agent)
    try:
        if parsed_user_agent := parse(apilog.user_agent):
            print(apilog.user_agent, parsed_user_agent)
            apilog.user_agent_browser_family = parsed_user_agent.browser.family
            apilog.user_agent_browser_version = parsed_user_agent.browser.version_string
            apilog.user_agent_os_family = parsed_user_agent.os.family
            apilog.user_agent_os_version = parsed_user_agent.os.version_string
            apilog.user_agent_device_family = parsed_user_agent.device.family
            apilog.user_agent_device_brand = parsed_user_agent.device.brand
            apilog.user_agent_device_model = parsed_user_agent.device.model
            apilog.is_mobile = parsed_user_agent.is_mobile
            apilog.is_tablet = parsed_user_agent.is_tablet
            apilog.is_pc = parsed_user_agent.is_pc
            apilog.is_touch_capable = parsed_user_agent.is_touch_capable
            apilog.is_bot = parsed_user_agent.is_bot
    except Exception as e:
        traceback.print_exc()
    return apilog

async def create_apilog(db: Session, user_project_id: uuid.UUID, apilog: APILogCreate, update_location: bool = False):
    db_apilog = APILog( **apilog.dict())
    db_apilog.user_project_id = user_project_id
    db_apilog.created_at = apilog.created_at or datetime.now()
    if update_location and apilog.ip_address:
        geolocation = await get_geolocation(apilog.ip_address)
        db_apilog.location = geolocation.get('city', '') + ', ' + geolocation.get('region', '') + ', ' + geolocation.get('country', '')
    
    if code := apilog.response_code:
        db_apilog.response_code_text = get_response_code_text(code)
    
    query_params = None
    if apilog.url:
        url, path, query_params = await get_url_components(apilog.url)
        db_apilog.path = path
    
    if apilog.user_agent:
        db_apilog = parse_user_agent(db_apilog)
    
    db.add(db_apilog)
    db.commit()
    db.refresh(db_apilog)
    if query_params:
        db.add_all(APILogQueryParam(api_log_id=db_apilog.id, key=key, value=value) for key, value in query_params.items() if key and value)
        db.commit()
    return db_apilog

async def create_apilog_bulk(db: Session, user_project_id: uuid.UUID, apilogs: List[APILogCreate], update_location: bool = False):
    db_apilogs = []
    for apilog in apilogs:
        if ca := await create_apilog(db, user_project_id, apilog, update_location):
            db_apilogs.append(ca)
    return db_apilogs


def get_counts_data(
    db: Session, 
    user_id: uuid.UUID, 
    project_id: uuid.UUID = None, 
    search_params = None
):
    query = db.query(APILog)
    
    query = query.filter(APILog.user_project_id == project_id)
    
    if search_params:
        if search_params.path:
            query = query.filter(APILog.path.ilike(f'{search_params.path}%'))
        if search_params.ip_address:
            query = query.filter(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.user_agent:
            query = query.filter(APILog.user_agent.ilike(f'{search_params.user_agent}%'))
        if search_params.location:
            query = query.filter(APILog.location.ilike(f'{search_params.location}%'))
        if search_params.response_code:
            query = query.filter(APILog.response_code == search_params.response_code)
    
    browser_family_counts = (
        query.with_entities(
            APILog.user_agent_browser_family,
            func.count(APILog.user_agent_browser_family)
        )
        .group_by(APILog.user_agent_browser_family)
        .all()
    )
    
    os_family_counts = (
        query.with_entities(
            APILog.user_agent_os_family,
            func.count(APILog.user_agent_os_family)
        )
        .group_by(APILog.user_agent_os_family)
        .all()
    )

    phone_count = query.filter(APILog.is_mobile == True).count()
    tablet_count = query.filter(APILog.is_tablet == True).count()
    pc_count = query.filter(APILog.is_pc == True).count()
    bot_count = query.filter(APILog.is_bot == True).count()
    other_count = query.filter(
        or_(
            APILog.is_mobile == False,
            APILog.is_tablet == False,
            APILog.is_pc == False,
            APILog.is_bot == False
        )
    ).count()

    device_type_counts = {
        "Phone": phone_count,
        "Tablet": tablet_count,
        "PC": pc_count,
        "Bot": bot_count,
        "Other": other_count
    }

    return {
        "browser_family_counts": dict(browser_family_counts),
        "os_family_counts": dict(os_family_counts),
        "device_type_counts": device_type_counts
    }



def get_apilogs(
    db: Session,
    user_id: uuid.UUID,
    page: int = 1,
    limit: int = 10,
    project_id: uuid.UUID = None,
    search_params: Optional[APILogSearch] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    sort_direction: Optional[str] = None
):
    offset = (page - 1) * limit
    
    if project_id:
        query = select(APILog).where(APILog.user_project_id == project_id)
    else:
        query = select(APILog).where(APILog.user_id == user_id)

    if search_params:
        if search_params.path:
            query = query.where(APILog.path.ilike(f'{search_params.path}%'))
        if search_params.ip_address:
            query = query.where(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.user_agent:
            query = query.where(APILog.user_agent.ilike(f'{search_params.user_agent}%'))
        if search_params.location:
            query = query.where(APILog.location.ilike(f'{search_params.location}%'))
        if search_params.response_code:
            query = query.where(APILog.response_code == search_params.response_code)

    if q:
        query = query.filter(
            or_(
                APILog.path.ilike(f'%{q}%'),
                APILog.user_agent.ilike(f'%{q}%'),
                APILog.ip_address.ilike(f'%{q}%'),
            )
        )

    # Total for query
    total_query = select(func.count()).select_from(query.subquery())
    total = db.execute(total_query).scalar()

    if sort:
        if sort == 'path':
            query = query.order_by(APILog.path.asc() if sort_direction == 'asc' else APILog.path.desc())
        elif sort == 'user_agent':
            query = query.order_by(APILog.user_agent.asc() if sort_direction == 'asc' else APILog.user_agent.desc())
        elif sort == 'ip_address':
            query = query.order_by(APILog.ip_address.asc() if sort_direction == 'asc' else APILog.ip_address.desc())
        elif sort == 'response_code':
            query = query.order_by(APILog.response_code.asc() if sort_direction == 'asc' else APILog.response_code.desc())
        elif sort == 'response_time':
            query = query.order_by(APILog.response_time.asc() if sort_direction == 'asc' else APILog.response_time.desc())
        elif sort == 'created_at':
            query = query.order_by(APILog.created_at.asc() if sort_direction == 'asc' else APILog.created_at.desc())
        else:
            query = query.order_by(APILog.created_at.desc())
    else:
        query = query.order_by(APILog.created_at.desc())

    query = query.offset(offset).limit(limit)

    results = db.execute(query).scalars().all()
    
    # Fetch query params for each log
    log_ids = [log.id for log in results]
    query_params = db.execute(
        select(APILogQueryParam).where(APILogQueryParam.api_log_id.in_(log_ids))
    ).scalars().all()
    
    # Group query params by log_id
    params_by_log_id = {}
    for param in query_params:
        if param.api_log_id not in params_by_log_id:
            params_by_log_id[param.api_log_id] = []
        params_by_log_id[param.api_log_id].append(param)

    # Attach query params to logs
    logs_with_params = []
    for log in results:
        log_dict = log.dict()
        log_dict["query_params"] = params_by_log_id.get(log.id, [])
        logs_with_params.append(log_dict)
    
    return {"logs": logs_with_params, "total": total}


def get_apilogs_stats(db: Session, user_id: uuid.UUID, project_id: uuid.UUID = None, search_params = None, frequency: str = "hour", q: Optional[str] = None):
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
        if search_params.path:
            query = query.filter(APILog.path.ilike(f'{search_params.path}%'))
        if search_params.ip_address:
            query = query.filter(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.user_agent:
            query = query.filter(APILog.user_agent.ilike(f'{search_params.user_agent}%'))
        if search_params.location:
            query = query.filter(APILog.location.ilike(f'{search_params.location}%'))
        if search_params.response_code:
            query = query.filter(APILog.response_code == search_params.response_code)

    if q:
        query = query.filter(
            or_(
                APILog.path.ilike(f'%{q}%'),
                APILog.user_agent.ilike(f'%{q}%'),
                APILog.ip_address.ilike(f'%{q}%'),
            )
        )

    stats_query = (
        query.with_entities(
            date_trunc.label('period'),
            func.count(case((APILog.response_code.between(200, 399), 1), else_=None)).label('success_count'),
            func.count(case((APILog.response_code < 200, 1), (APILog.response_code >= 400, 1), else_=None)).label('error_count'),
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
