from fastapi import FastAPI, Request
from app.database import create_db_and_tables
from app.routers import auth, apikey, apilog, botinfo
from app.models.user import User, UserProject
from app.models.apilog import APILog
from sqlmodel import select, Session
from app.database import create_db_and_tables, engine
from app.crud.apilog import get_geolocation
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import get_session
import httpx
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from app.config import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
import time
import uuid

app = FastAPI(
    title="WhoWhyWhen API",
    description="API for WhoWhyWhen",
    version="0.1.0",
    # docs_url="/",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Every hour, check if the user's monthly credit limit has been exceeded since monthly_credit_limit_reset. If so, set the flag for the user.monthly_credit_usage_crossed = True. 
    # If monthly_credit_limit_reset has crossed a month, reset the flag to False and reset the value of monthly_credit_limit_reset to the current date.
    @repeat_every(seconds=3600)
    async def check_monthly_credit_limit():
        print("Checking monthly credit limit...")
        for user in app.state.db.query(User).all():
            print(f"Checking user {user.email}...")
            db = next(get_session())
            # Get total requests count since monthly_credit_limit_reset. For each Project the user has, add the total count to the total_requests_count variable.
            total_requests_count = 0
            for project in user.projects:
                total_requests_count += db.query(APILog).filter(APILog.user_project_id == project.id, APILog.created_at >= user.monthly_credit_limit_reset).count()

            print(f"Total requests count: {total_requests_count}")
            print(f"Monthly credit limit: {user.monthly_credit_limit}")
            
            # If the total_requests_count is greater than the user's monthly_credit_limit, set the user's monthly_credit_usage_crossed flag to True.
            if total_requests_count > user.monthly_credit_limit:
                user.monthly_credit_usage_crossed = True
            
            # If the user's monthly_credit_limit_reset has crossed a month, reset the user's monthly_credit_usage_crossed flag to False, reset the value of monthly_credit_limit_reset to the current date, and reset the total_requests_count to 0.
            if datetime.now() - user.monthly_credit_limit_reset > timedelta(days=30):
                user.monthly_credit_usage_crossed = False
                user.monthly_credit_limit_reset = datetime.now()
            
            db.add(user)
            db.commit()
            db.refresh(user)

# Add CORS middleware
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
        endpoint = request.url.path
        # User agent as request info
        request_info = request.headers.get("User-Agent")
        response_code = response.status_code
        response_time = (end_time - start_time).total_seconds()
        
        async with get_session() as session:
            project_id = uuid.UUID("8adfc1db-5112-41a9-b747-657302e9c5d4") 
            geolocation = await get_geolocation(ip_address)
            location = f"{geolocation.get('ip', '')}, {geolocation.get('city', '')}, {geolocation.get('region', '')}"

            apilog = APILog(
                user_project_id=project_id,
                endpoint=endpoint,
                ip_address=ip_address,
                request_info=request_info,
                location=location,
                response_code=response_code,
                response_time=response_time,
                created_at=start_time,
            )

            session.add(apilog)
            session.commit()

        return response
    
app.add_middleware(APILogMiddleware)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/api/ip-location")
async def get_ip_location(request: Request):
    ip = request.state.ip
    return {"ip": ip}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(apikey.router, prefix="/api", tags=["apikey"])
app.include_router(apilog.router, prefix="/api", tags=["apilog"])
app.include_router(botinfo.router, prefix="/api", tags=["botinfo"])
