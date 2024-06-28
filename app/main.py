from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, apikey, apilog, botinfo
from app.models.user import User
from sqlmodel import select, Session
from app.database import create_db_and_tables, engine
from app.crud.user import reset_request_count_if_needed

app = FastAPI(
    title="WhoWhyWhen API",
    description="API for WhoWhyWhen",
    version="0.1.0",
    docs_url="/",
)

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

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(apikey.router, prefix="/api", tags=["apikey"])
app.include_router(apilog.router, prefix="/api", tags=["apilog"])
app.include_router(botinfo.router, prefix="/api", tags=["botinfo"])
