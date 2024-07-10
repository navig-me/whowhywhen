from fastapi import FastAPI, Request, BackgroundTasks
from app.database import create_db_and_tables, get_session
from app.routers import auth, apikey, apilog, botinfo
from app.models.user import User
from app.models.apilog import APILog, APILogQueryParam
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from app.crud.apilog import get_geolocation, get_url_components
import uuid
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="WhoWhyWhen API",
    description="API for WhoWhyWhen",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.ip = request.client.host
        response = await call_next(request)
        return response

app.add_middleware(IPMiddleware)

class APILogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()

        ip_address = request.client.host
        url = str(request.url)
        user_agent = request.headers.get("User-Agent")
        response_code = response.status_code
        response_time = (end_time - start_time).total_seconds()
        
        query_params = None
        if url:
            _, path, query_params = await get_url_components(url)

        background_tasks = request.state.background_tasks
        background_tasks.add_task(
            self.log_to_db,
            ip_address,
            url,
            path,
            user_agent,
            response_code,
            response_time,
            start_time,
            query_params,
        )

        return response

    async def log_to_db(
        self,
        ip_address,
        url,
        path,
        user_agent,
        response_code,
        response_time,
        start_time,
        query_params,
    ):
        session = next(get_session())
        project_id = uuid.UUID("20bd946c-a24e-4f92-a3ff-e30c8f36794c")
        # geolocation = await get_geolocation(ip_address)
        # location = f"{geolocation.get('city', '')}, {geolocation.get('region', '')}, {geolocation.get('country', '')}"

        apilog = APILog(
            user_project_id=project_id,
            url=url,
            path=path,
            ip_address=ip_address,
            user_agent=user_agent,
            location=None,
            response_code=response_code,
            response_time=response_time,
            created_at=start_time,
        )

        session.add(apilog)
        session.commit()
        session.refresh(apilog)

        if query_params:
            session.add_all(
                APILogQueryParam(api_log_id=apilog.id, key=key, value=value)
                for key, value in query_params.items() if key and value
            )
            session.commit()

app.add_middleware(APILogMiddleware)

@app.middleware("http")
async def add_background_tasks(request: Request, call_next):
    request.state.background_tasks = BackgroundTasks()
    response = await call_next(request)
    response.background = request.state.background_tasks
    return response

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(apilog.router_api, prefix="/api", tags=["apilog"])
