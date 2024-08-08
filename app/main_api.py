import logging
import uuid
from datetime import datetime

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.crud.apilog import create_apilog
from app.database import get_session
from app.models.apilog import APILog, APILogQueryParam
from app.models.botinfo import BotInfo
from app.models.user import User, UserProject
from app.routers import apilog

logger = logging.getLogger(__name__)

app = FastAPI(
    title="WhoWhyWhen API",
    description="API for WhoWhyWhen - Supercharge your APIsm",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
        
        background_tasks = request.state.background_tasks
        background_tasks.add_task(
            self.log_to_db,
            ip_address,
            url,
            user_agent,
            response_code,
            response_time,
        )

        return response

    async def log_to_db(
        self,
        ip_address,
        url,
        user_agent,
        response_code,
        response_time,
    ):
        session = next(get_session())
        project_id = uuid.UUID("20bd946c-a24e-4f92-a3ff-e30c8f36794c")

        apilog = APILog(
            user_project_id=project_id,
            url=url,
            ip_address=ip_address,
            user_agent=user_agent,
            response_code=response_code,
            response_time=response_time,
        )

        await create_apilog(session, project_id, apilog)


app.add_middleware(APILogMiddleware)

@app.middleware("http")
async def add_background_tasks(request: Request, call_next):
    request.state.background_tasks = BackgroundTasks()
    response = await call_next(request)
    response.background = request.state.background_tasks
    return response

app.include_router(apilog.router_api, prefix="/api", tags=["apilog"])
