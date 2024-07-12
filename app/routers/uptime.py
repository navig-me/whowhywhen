from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from typing import List, Optional
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlmodel import Session
from app.database import get_session
from app.models.user import UserProject
from app.models.uptime import UptimeMonitor, UptimeMonitorStatus, MonitorType
import uuid
from app.schemas.uptime import MonitorCreate, MonitorUpdate


router = APIRouter()

@router.post("/projects/{project_id}/monitors/", response_model=UptimeMonitor)
def create_monitor(project_id: uuid.UUID, monitor: MonitorCreate, session: Session = Depends(get_session)):
    project = session.get(UserProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    new_monitor = UptimeMonitor(
        name=monitor.name,
        url=monitor.url,
        type=monitor.type,
        check_interval=monitor.check_interval,
        project_id=project_id
    )
    session.add(new_monitor)
    session.commit()
    session.refresh(new_monitor)
    return new_monitor

@router.get("/projects/{project_id}/monitors/", response_model=List[UptimeMonitor])
def get_monitors(project_id: uuid.UUID, session: Session = Depends(get_session)):
    project = session.get(UserProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return session.exec(select(UptimeMonitor).where(UptimeMonitor.project_id == project_id)).all()

@router.get("/monitors/{monitor_id}", response_model=UptimeMonitor)
def get_monitor(monitor_id: uuid.UUID, session: Session = Depends(get_session)):
    monitor = session.get(UptimeMonitor, monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return monitor

@router.put("/monitors/{monitor_id}", response_model=UptimeMonitor)
def update_monitor(monitor_id: uuid.UUID, monitor_update: MonitorUpdate, session: Session = Depends(get_session)):
    monitor = session.get(UptimeMonitor, monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    for key, value in monitor_update.dict(exclude_unset=True).items():
        setattr(monitor, key, value)
    
    monitor.modified = datetime.now()
    session.add(monitor)
    session.commit()
    session.refresh(monitor)
    return monitor

@router.delete("/monitors/{monitor_id}", response_model=dict)
def delete_monitor(monitor_id: uuid.UUID, session: Session = Depends(get_session)):
    monitor = session.get(UptimeMonitor, monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    session.delete(monitor)
    session.commit()
    return {"message": "Monitor deleted successfully"}


@router.post("/monitors/status/{monitor_id}") 
def get_monitor_status(monitor_id: uuid.UUID, start_datetime: Optional[datetime] = None, end_datetime: Optional[datetime] = None, session: Session = Depends(get_session)):
    monitor = session.get(UptimeMonitor, monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    
    if start_datetime:
        query = select(UptimeMonitorStatus).where(UptimeMonitorStatus.monitor_id == monitor_id).where(UptimeMonitorStatus.created >= start_datetime)
    elif end_datetime:
        query = select(UptimeMonitorStatus).where(UptimeMonitorStatus.monitor_id == monitor_id).where(UptimeMonitorStatus.created <= end_datetime)
    else:
        query = select(UptimeMonitorStatus).where(UptimeMonitorStatus.monitor_id == monitor_id)
    
    results = session.exec(query).all()
    
    full_periods = []
    current_period = start_datetime
    while current_period <= end_datetime:
        full_periods.append(current_period.strftime("%Y-%m-%d %H:%M"))
        if monitor.type == MonitorType.ping:
            current_period += timedelta(minutes=1)
        elif monitor.type == MonitorType.http:
            current_period += timedelta(hours=1)
        elif monitor.type == MonitorType.https:
            current_period += timedelta(days=1)
        else:
            current_period += timedelta(hours=1)

    results = session.exec(query).all()

    full_results = [{"period": period, "up_count": up_count, "down_count": down_count, "unknown_count": unknown_count} for period, up_count, down_count, unknown_count in results]

    return full_results
