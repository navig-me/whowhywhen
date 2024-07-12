from fastapi import FastAPI, Request, BackgroundTasks
from app.database import create_db_and_tables, get_session
from app.routers import auth, apikey, apilog, botinfo, uptime
from app.models.user import User
from app.models.apilog import APILog, APILogQueryParam
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from app.crud.apilog import get_geolocation, get_url_components, create_apilog
import uuid
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="WhoWhyWhen Dashboard",
    description="Dashboard for WhoWhyWhen",
    version="0.1.0",
    docs_url='/docsnonpublic',
    redoc_url=None
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    @repeat_every(seconds=3600)
    async def check_monthly_credit_limit():
        print("Checking monthly credit limit...")
        for user in app.state.db.query(User).all():
            print(f"Checking user {user.email}...")
            db = next(get_session())
            total_requests_count = 0
            for project in user.projects:
                total_requests_count += db.query(APILog).filter(APILog.user_project_id == project.id, APILog.created_at >= user.monthly_credit_limit_reset).count()
            print(f"Total requests count: {total_requests_count}")
            print(f"Monthly credit limit: {user.monthly_credit_limit}")
            if total_requests_count > user.monthly_credit_limit:
                user.monthly_credit_usage_crossed = True
            if datetime.now() - user.monthly_credit_limit_reset > timedelta(days=30):
                user.monthly_credit_usage_crossed = False
                user.monthly_credit_limit_reset = datetime.now()
            db.add(user)
            db.commit()
            db.refresh(user)

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
        project_id = uuid.UUID("6863eb74-b5e8-4253-b7b0-2275e46c678f")

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

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/dashapi/ip-location")
async def get_ip_location(request: Request):
    ip = request.state.ip
    return {"ip": ip}

app.include_router(auth.router, prefix="/dashauth", tags=["auth"])
app.include_router(apikey.router, prefix="/dashapi", tags=["apikey"])
app.include_router(apilog.router_dash, prefix="/dashapi", tags=["apilog"])
app.include_router(botinfo.router, prefix="/dashapi", tags=["botinfo"])
app.include_router(uptime.router, prefix="/dashapi", tags=["uptime"])
