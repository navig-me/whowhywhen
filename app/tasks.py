import httpx
from app.appcelery import Celery
from datetime import datetime
from sqlmodel import Session, select
from app.database import get_session
from app.models.uptime import UptimeMonitor, UptimeMonitorStatus, MonitorStatus, MonitorType

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def check_monitor(monitor_id: str):
    session = next(get_session())
    monitor = session.get(UptimeMonitor, monitor_id)
    
    if not monitor:
        return

    status = MonitorStatus.unknown
    response_time = None
    response_code = None
    response_code_text = None

    try:
        if monitor.type in [MonitorType.http, MonitorType.https]:
            start_time = datetime.now()
            response = httpx.get(monitor.url)
            response_time = (datetime.now() - start_time).total_seconds()
            response_code = response.status_code
            response_code_text = response.reason_phrase
            status = MonitorStatus.up if response.status_code == 200 else MonitorStatus.down
        elif monitor.type == MonitorType.ping:
            # Implement ping logic here
            pass
    except Exception as e:
        status = MonitorStatus.down
        response_code_text = str(e)

    monitor_status = UptimeMonitorStatus(
        monitor_id=monitor.id,
        status=status,
        response_time=response_time,
        response_code=response_code,
        response_code_text=response_code_text,
    )
    session.add(monitor_status)
    monitor.modified = datetime.now()
    monitor.status = status
    session.commit()
    session.refresh(monitor)

@celery_app.task
def check_all_monitors():
    session = next(get_session())
    monitors = session.exec(select(UptimeMonitor)).all()
    for monitor in monitors:
        check_monitor.delay(monitor.id)

@celery_app.task
def schedule_monitor_check(monitor_id: str, interval: int):
    check_monitor.apply_async(args=[monitor_id], countdown=interval * 60)
