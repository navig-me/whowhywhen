from fastapi import FastAPI, Request
from app.database import create_db_and_tables
from app.routers import auth, apikey, apilog, botinfo
from app.models.user import User
from sqlmodel import select, Session
from app.database import create_db_and_tables, engine
from app.crud.user import reset_request_count_if_needed
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

app = FastAPI(
    title="WhoWhyWhen API",
    description="API for WhoWhyWhen",
    version="0.1.0",
    docs_url="/",
)

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


def reset_request_counts_periodically():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            reset_request_count_if_needed(user)
        session.commit()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    reset_request_counts_periodically()

async def get_geolocation(ip: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://ipinfo.io/{ip}/json')
        return response.json()

@app.get("/api/ip-location")
async def get_ip_location(request: Request):
    ip = request.state.ip
    location_data = await get_geolocation(ip)
    complete_location_name = location_data.get('city', '') + ', ' + location_data.get('region', '')
    location_name = complete_location_name.replace(',', '').replace(' ', '')
    return {"ip": ip, "location": location_name}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(apikey.router, prefix="/api", tags=["apikey"])
app.include_router(apilog.router, prefix="/api", tags=["apilog"])
app.include_router(botinfo.router, prefix="/api", tags=["botinfo"])
