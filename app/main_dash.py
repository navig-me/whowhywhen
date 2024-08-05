import asyncio
import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from user_agents import parse

from app.crud.apilog import create_apilog
from app.database import create_db_and_tables, get_session
from app.models.apilog import APILog
from app.models.user import User, UserAlertConfig, UserProject
from app.routers import apikey, apilog, auth, botinfo, event, alert
from app.services.monitoring_service import check_services
from app.services.stripe_service import get_subscription_end_date
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = next(get_session())
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

async def check_alerts():
    while True:
        print("Checking alerts...")
        with session_scope() as db:
            try:
                user_projects = db.query(UserProject).all()
                for user_project in user_projects:
                    alert_config = db.query(UserAlertConfig).filter(UserAlertConfig.user_project_id == user_project.id).first()
                    if not alert_config:
                        alert_config = UserAlertConfig(user_project_id=user_project.id)
                        db.add(alert_config)
                        db.commit()
                        db.refresh(alert_config)
                    print("Checking alert config for ...", user_project)
                    check_services(alert_config, db)
            except Exception as e:
                logger.error(f"Error in check_alerts: {e}")
        await asyncio.sleep(300)  # 5 minutes

async def check_monthly_credit_limit():
    while True:
        print("Checking monthly credit limit...")
        db = next(get_session())
        try:
            for user in db.query(User).all():
                print(f"Checking user {user.email}...")
                total_requests_count = 0
                for project in user.projects:
                    total_requests_count += db.query(APILog).filter(
                        APILog.user_project_id == project.id,
                        APILog.created_at >= user.monthly_credit_limit_reset
                    ).count()
                print(f"Total requests count: {total_requests_count}")
                print(f"Monthly credit limit: {user.monthly_credit_limit}")
                if total_requests_count > user.monthly_credit_limit:
                    user.monthly_credit_usage_crossed = True
                
                # Get the subscription end date from Stripe
                subscription_end_date = get_subscription_end_date(user)
                
                if subscription_end_date and datetime.now() > subscription_end_date:
                    user.monthly_credit_usage_crossed = False
                    user.monthly_credit_limit_reset = datetime.now()
                db.add(user)
                db.commit()
                db.refresh(user)
        except Exception as e:
            logger.error(f"Error in check_monthly_credit_limit: {e}")
        finally:
            db.close()
        await asyncio.sleep(600)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Ensure this is uncommented if you want to create DB and tables on startup
    app.state.db = next(get_session())
    task = asyncio.create_task(check_monthly_credit_limit())
    task2 = asyncio.create_task(check_alerts())
    yield
    task.cancel()
    task2.cancel()
    app.state.db.close()

app = FastAPI(
    title="WhoWhyWhen Dashboard",
    description="Dashboard for WhoWhyWhen",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
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

@app.get("/dashapi/ip-location")
async def get_ip_location(request: Request):
    ip = request.state.ip
    return {"ip": ip}

@app.get("/dashapi/device-details")
async def get_device_details(request: Request):
    user_agent_str = request.headers.get("User-Agent")
    if not user_agent_str:
        return {"error": "User-Agent header not found"}
    
    user_agent = parse(user_agent_str)
    device_details = {
        "browser": user_agent.browser.family,
        "browser_version": user_agent.browser.version_string,
        "os": user_agent.os.family,
        "os_version": user_agent.os.version_string,
        "device": user_agent.device.family,
        "is_mobile": user_agent.is_mobile,
        "is_tablet": user_agent.is_tablet,
        "is_pc": user_agent.is_pc,
        "is_bot": user_agent.is_bot,
    }
    return device_details

app.include_router(auth.router, prefix="/dashauth", tags=["auth"])
app.include_router(apikey.router, prefix="/dashapi", tags=["apikey"])
app.include_router(apilog.router_dash, prefix="/dashapi", tags=["apilog"])
app.include_router(botinfo.router, prefix="/dashapi", tags=["botinfo"])
app.include_router(event.router_event, prefix="/dashapi", tags=["event"])
app.include_router(alert.router, prefix="/dashapi", tags=["alert"])
