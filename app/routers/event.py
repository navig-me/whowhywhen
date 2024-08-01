# routers/event.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_session
from app.models.apilog import APILog
from app.crud.apilog import get_events, count_events

router_event = APIRouter()

@router_event.get("/events", summary="Get Events", description="Retrieve recorded events with pagination.", tags=["Events"])
async def get_events_endpoint(
    type_filter: Optional[str] = Query(None, description="Filter events by type: 'endpoints', 'bots', or 'both'"),
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """
    Retrieve recorded events with pagination and optional filtering by type.
    """
    if type_filter not in ["endpoints", "bots", None]:
        return {"error": "Invalid type_filter value. Valid values are 'endpoints', 'bots', or 'both'."}
    
    events = get_events(session, type_filter, offset, limit)
    total = count_events(session, type_filter)
    return {"total": total, "events": events}
