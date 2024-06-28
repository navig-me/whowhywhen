from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
import bcrypt
from datetime import datetime, timedelta

FREE_PLAN_LIMIT = 10000
PAID_PLAN_LIMIT = 100000

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password, domain=user.domain)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()



def reset_request_count_if_needed(user: User):
    now = datetime.now()
    if now.month != user.last_request_reset.month or now.year != user.last_request_reset.year:
        user.request_count = 0
        user.last_request_reset = now

def increment_request_count(user: User, db: Session):
    reset_request_count_if_needed(user)
    if user.subscription_plan == "free" and user.request_count >= FREE_PLAN_LIMIT:
        raise HTTPException(status_code=403, detail="Request limit exceeded for free plan")
    elif user.subscription_plan == "paid" and user.request_count >= PAID_PLAN_LIMIT:
        raise HTTPException(status_code=403, detail="Request limit exceeded for paid plan")
    user.request_count += 1
    db.add(user)
    db.commit()
    db.refresh(user)
