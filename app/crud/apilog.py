import re
import traceback
import uuid
from datetime import datetime, timedelta
from http.client import responses
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

import httpx
from relative_datetime import DateTimeUtils
from sqlalchemy import and_, case, func, or_, select
from sqlalchemy.sql import case, exists, func
from sqlmodel import Session, or_, select
from user_agents import parse

from app.models.apilog import APILog, APILogQueryParam
from app.models.botinfo import BotInfo
from app.models.user import UserProject
from app.schemas.apilog import APILogCreate, APILogSearch


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

bot_infos = []

def get_bot_id(user_agent: str, session: Session):
    global bot_infos
    if not bot_infos:
        bot_infos_query = session.query(BotInfo).all()
        bot_infos = [bot_info.dict() for bot_info in bot_infos_query]
    # Check if any of botinfo.pattern matches the user agent
    for botinfo in bot_infos:
        if pattern := botinfo.get('pattern'):
            compiled_pattern = re.compile(pattern)
            if compiled_pattern.search(user_agent):
                return botinfo.get("id")
    return None

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
        db_apilog.bot_id = get_bot_id(apilog.user_agent, db)
    
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

def get_bot_logs_stats_data(
    db: Session, 
    user_id: uuid.UUID, 
    project_id: uuid.UUID = None, 
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
):
    print("Getting bot logs stats data...", user_id, project_id, start_datetime, end_datetime)
    end_date = end_datetime if end_datetime else datetime.now()
    start_date = start_datetime if start_datetime else end_date - timedelta(days=30)

    # Initial query to filter based on user, project, and date range
    query = db.query(APILog).filter(
        APILog.user_project_id == project_id,
        APILog.created_at >= start_date,
        APILog.created_at <= end_date
    )
    if project_id:
        query = query.filter(APILog.user_project_id == project_id)
    
    top_bots = (
        query.with_entities(APILog.bot_id, func.count(APILog.bot_id).label('count'))
        .filter(APILog.is_bot == True)
        .group_by(APILog.bot_id)
        .order_by(func.count(APILog.bot_id).desc())
        .limit(20)
        .all()
    )
    
    # Collect bot stats
    bot_stats = []
    for bot_id, count in top_bots:
        bot_info = db.query(BotInfo).filter(BotInfo.id == bot_id).first()
        if not bot_info:
            continue
        
        # Device stats
        device_stats = (
            query.with_entities(
                func.count(case((APILog.is_mobile == True, 1))).label('mobile_count'),
                func.count(case((APILog.is_tablet == True, 1))).label('tablet_count'),
                func.count(case((APILog.is_pc == True, 1))).label('pc_count')
            )
            .filter(APILog.bot_id == bot_id)
            .first()
        )

        # Top 10 endpoints called
        top_10_endpoints = (
            query.with_entities(APILog.path, func.count(APILog.path).label('count'))
            .filter(APILog.bot_id == bot_id)
            .group_by(APILog.path)
            .order_by(func.count(APILog.path).desc())
            .limit(10)
            .all()
        )
        top_10_endpoints = [{'path': endpoint.path, 'count': endpoint.count} for endpoint in top_10_endpoints]

        # Top 10 response statuses
        top_response_statuses = (
            query.with_entities(APILog.response_code, func.count(APILog.response_code).label('count'))
            .filter(APILog.bot_id == bot_id)
            .group_by(APILog.response_code)
            .order_by(func.count(APILog.response_code).desc())
            .limit(10)
            .all()
        )
        top_response_statuses = {status: count for status, count in top_response_statuses}

        last_seen = query.filter(APILog.bot_id == bot_id).order_by(APILog.created_at.desc()).first().created_at
        relative_time, direction = DateTimeUtils.relative_datetime(last_seen)

        bot_stats.append({
            'bot_id': bot_id,
            'bot_name': bot_info.bot_name,
            'bot_website': bot_info.website,
            'total_api_calls': count,
            'device_stats': {
                'mobile': device_stats.mobile_count,
                'tablet': device_stats.tablet_count,
                'pc': device_stats.pc_count
            },
            'top_10_endpoints': top_10_endpoints,
            'top_response_statuses': top_response_statuses,
            'last_seen': last_seen,
            'last_seen_text': f"{relative_time} ago",
            'pattern': bot_info.pattern
        })

    return {'bot_stats': bot_stats}

def coalesce_to_other(column):
    return func.coalesce(column, 'Other')

def get_counts_data(
    db: Session, 
    user_id: uuid.UUID, 
    project_id: uuid.UUID = None, 
    search_params = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    bots_only: bool = False  # Add this parameter
):
    query = db.query(APILog)
    
    query = query.filter(APILog.user_project_id == project_id)
    
    if start_datetime:
        query = query.filter(APILog.created_at >= start_datetime)
    if end_datetime:
        query = query.filter(APILog.created_at <= end_datetime)

    if search_params:
        if search_params.path:
            query = query.filter(APILog.path.ilike(f'{search_params.path}%'))
        if search_params.ip_address:
            query = query.filter(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.user_agent:
            query = query.filter(APILog.user_agent.ilike(f'%{search_params.user_agent}%'))
        if search_params.location:
            query = query.filter(APILog.location.ilike(f'{search_params.location}%'))
        if search_params.response_code:
            query = query.filter(APILog.response_code == search_params.response_code)

    if bots_only:
        query = query.filter(APILog.is_bot == True)  # Add the bots_only filter

    browser_family_counts = (
        query.with_entities(
            coalesce_to_other(APILog.user_agent_browser_family).label('browser_family'),
            func.count(APILog.user_agent_browser_family)
        )
        .filter(APILog.is_bot == False)
        .group_by('browser_family')
        .all()
    )
    
    os_family_counts = (
        query.with_entities(
            coalesce_to_other(APILog.user_agent_os_family).label('os_family'),
            func.count(APILog.user_agent_os_family)
        )
        .filter(APILog.is_bot == False)
        .group_by('os_family')
        .all()
    )

    # User agent counts (Get top 10 and add others)
    user_agent_counts = (
        query.with_entities(
            coalesce_to_other(APILog.user_agent).label('user_agent'),
            func.count(APILog.user_agent)
        )
        .filter(APILog.is_bot == False)
        .group_by('user_agent')
        .order_by(func.count(APILog.user_agent).desc())
        .all()
    )

    # Process the user agent counts to get top 10 and aggregate others
    top_15_user_agents = user_agent_counts[:10]
    others_count = sum(count for _, count in user_agent_counts[10:])
    if others_count > 0:
        top_15_user_agents.append(('Other', others_count))

    top_15_user_agent_counts = dict(top_15_user_agents)

    response_code_counts = (
        query.with_entities(
            APILog.response_code.label('response_code'),
            func.count(APILog.response_code)
        )
        .group_by('response_code')
        .all()
    )
    response_code_counts = dict(response_code_counts)
    response_code_counts_keyed = dict()
    for key, value in response_code_counts.items():
        response_code_counts_keyed[f"{key} ({get_response_code_text(key)})"] = value

    phone_count = query.filter(APILog.is_mobile == True).count()
    tablet_count = query.filter(APILog.is_tablet == True).count()
    pc_count = query.filter(APILog.is_pc == True).count()
    bot_count = query.filter(APILog.is_bot == True).count()
    other_count = query.filter(
        or_(
            APILog.is_mobile == False,
            APILog.is_mobile == None,
            APILog.is_tablet == False,
            APILog.is_tablet == None,
            APILog.is_pc == False,
            APILog.is_pc == None,
            APILog.is_bot == False,
            APILog.is_bot == None
        )
    ).count()

    device_type_counts = {
        "Phone": phone_count,
        "Tablet": tablet_count,
        "PC": pc_count,
        "Bot": bot_count,
        "Other": other_count
    }

    # get the Browser Family counts where is_bot is True
    bot_browser_family_counts = (
        query.with_entities(
            coalesce_to_other(APILog.user_agent_browser_family).label('browser_family'),
            func.count(APILog.user_agent_browser_family)
        )
        .group_by('browser_family')
        .filter(APILog.is_bot == True)
        .all()
    )

    return {
        "browser_family_counts": dict(browser_family_counts),
        "os_family_counts": dict(os_family_counts),
        "device_type_counts": dict(device_type_counts),
        "response_code_counts": dict(response_code_counts_keyed),
        "bot_browser_family_counts": dict(bot_browser_family_counts),
        "user_agent_counts": top_15_user_agent_counts
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
    sort_direction: Optional[str] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    bots_only: bool = False  # Add this parameter
):
    offset = (page - 1) * limit
    
    if project_id:
        query = select(APILog).where(APILog.user_project_id == project_id)
    else:
        query = select(APILog).where(APILog.user_id == user_id)

    if start_datetime:
        query = query.where(APILog.created_at >= start_datetime)
    if end_datetime:
        query = query.where(APILog.created_at <= end_datetime)

    if search_params:
        if search_params.path:
            query = query.where(APILog.path.ilike(f'{search_params.path}%'))
        if search_params.ip_address:
            query = query.where(APILog.ip_address.ilike(f'{search_params.ip_address}%'))
        if search_params.user_agent:
            query = query.where(APILog.user_agent.ilike(f'%{search_params.user_agent}%'))
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

    if bots_only:
        query = query.where(APILog.is_bot == True)  # Add the bots_only filter

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
    
    log_ids = [log.id for log in results]
    query_params = db.execute(
        select(APILogQueryParam).where(APILogQueryParam.api_log_id.in_(log_ids))
    ).scalars().all()
    
    params_by_log_id = {}
    for param in query_params:
        if param.api_log_id not in params_by_log_id:
            params_by_log_id[param.api_log_id] = []
        params_by_log_id[param.api_log_id].append(param)

    logs_with_params = []
    for log in results:
        log_dict = log.dict()
        # response_time to 5 decimal places
        if log_dict["response_time"]:
            log_dict["response_time"] = round(log_dict["response_time"], 5)
        log_dict["query_params"] = params_by_log_id.get(log.id, [])

        if log.bot_id:
            log_dict["bot_id"] = log.bot_id
            if bot_info := db.query(BotInfo).filter(BotInfo.id == log.bot_id).first():
                log_dict["bot_data"] = bot_info.dict()

        logs_with_params.append(log_dict)
    
    return {"logs": logs_with_params, "total": total}


def get_apilogs_stats(
    db: Session, 
    user_id: uuid.UUID, 
    project_id: uuid.UUID = None, 
    search_params = None, 
    frequency: str = "hour", 
    q: Optional[str] = None, 
    start_datetime: Optional[datetime] = None, 
    end_datetime: Optional[datetime] = None,
    bots_only: bool = False  # Add this parameter
):
    end_date = end_datetime if end_datetime else datetime.now()

    if frequency == "minute":
        start_date = start_datetime if start_datetime else end_date - timedelta(hours=1)
        period_fmt = '%Y-%m-%d %H:%M'
        date_trunc = func.date_trunc('minute', APILog.created_at)
    elif frequency == "day":
        start_date = start_datetime if start_datetime else end_date - timedelta(days=30)
        period_fmt = '%Y-%m-%d'
        date_trunc = func.date_trunc('day', APILog.created_at)
    else:  # Default to hourly data
        start_date = start_datetime if start_datetime else end_date - timedelta(hours=24)
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
            query = query.filter(APILog.user_agent.ilike(f'%{search_params.user_agent}%'))
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

    if bots_only:
        query = query.filter(APILog.is_bot == True)  # Add the bots_only filter

    stats_query = (
        query.with_entities(
            date_trunc.label('period'),
            func.count(case((APILog.response_code.between(200, 299), 1), else_=None)).label('2xx_count'),
            func.count(case((APILog.response_code.between(300, 399), 1), else_=None)).label('3xx_count'),
            func.count(case((APILog.response_code.between(400, 499), 1), else_=None)).label('4xx_count'),
            func.count(case((APILog.response_code.between(500, 599), 1), else_=None)).label('5xx_count'),
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
    
    counts = {result[0].strftime(period_fmt): {"2xx_count": result[1], "3xx_count": result[2], "4xx_count": result[3], "5xx_count": result[4], "avg_response_time": result[5]} for result in results}
    full_results = [{"period": period, "2xx_count": counts.get(period, {}).get("2xx_count", 0), "3xx_count": counts.get(period, {}).get("3xx_count", 0), "4xx_count": counts.get(period, {}).get("4xx_count", 0), "5xx_count": counts.get(period, {}).get("5xx_count", 0), "avg_response_time": counts.get(period, {}).get("avg_response_time", 0)} for period in full_periods]
    
    return full_results


def get_events(session: Session, type_filter: str, offset: int = 0, limit: int = 10) -> List[APILog]:
    # Subqueries to get the first occurrence of each new endpoint or bot
    subquery_endpoints = (
        session.query(
            APILog.path,
            func.min(APILog.created).label("first_seen")
        )
        .filter(APILog.response_code.between(200, 299))
        .group_by(APILog.path)
        .subquery()
    )

    subquery_bots = (
        session.query(
            APILog.bot_id,
            func.min(APILog.created).label("first_seen")
        )
        .filter(APILog.response_code.between(200, 299))
        .group_by(APILog.bot_id)
        .subquery()
    )

    events_query = session.query(APILog)

    if type_filter == "endpoints":
        events_query = events_query.filter(
            exists().where(
                and_(
                    APILog.path == subquery_endpoints.c.path,
                    APILog.created == subquery_endpoints.c.first_seen
                )
            )
        )
    elif type_filter == "bots":
        events_query = events_query.filter(
            exists().where(
                and_(
                    APILog.bot_id == subquery_bots.c.bot_id,
                    APILog.created == subquery_bots.c.first_seen
                )
            )
        )
    else:
        events_query = events_query.filter(
            or_(
                exists().where(
                    and_(
                        APILog.path == subquery_endpoints.c.path,
                        APILog.created == subquery_endpoints.c.first_seen
                    )
                ),
                exists().where(
                    and_(
                        APILog.bot_id == subquery_bots.c.bot_id,
                        APILog.created == subquery_bots.c.first_seen
                    )
                )
            )
        )

    events_query = events_query.order_by(APILog.created).offset(offset).limit(limit)

    return events_query.all()


def count_events(session: Session, type_filter: str) -> int:
    # Subqueries to get the first occurrence of each new endpoint or bot
    subquery_endpoints = (
        session.query(
            APILog.path,
            func.min(APILog.created).label("first_seen")
        )
        .filter(APILog.response_code.between(200, 299))
        .group_by(APILog.path)
        .subquery()
    )

    subquery_bots = (
        session.query(
            APILog.bot_id,
            func.min(APILog.created).label("first_seen")
        )
        .filter(APILog.response_code.between(200, 299))
        .group_by(APILog.bot_id)
        .subquery()
    )

    count_query = session.query(APILog.id)

    if type_filter == "endpoints":
        count_query = count_query.filter(
            exists().where(
                and_(
                    APILog.path == subquery_endpoints.c.path,
                    APILog.created == subquery_endpoints.c.first_seen
                )
            )
        )
    elif type_filter == "bots":
        count_query = count_query.filter(
            exists().where(
                and_(
                    APILog.bot_id == subquery_bots.c.bot_id,
                    APILog.created == subquery_bots.c.first_seen
                )
            )
        )
    else:
        count_query = count_query.filter(
            or_(
                exists().where(
                    and_(
                        APILog.path == subquery_endpoints.c.path,
                        APILog.created == subquery_endpoints.c.first_seen
                    )
                ),
                exists().where(
                    and_(
                        APILog.bot_id == subquery_bots.c.bot_id,
                        APILog.created == subquery_bots.c.first_seen
                    )
                )
            )
        )

    return count_query.count()
