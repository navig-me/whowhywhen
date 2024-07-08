from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user import User, UserProject
from app.schemas.user import UserCreate
import bcrypt
from datetime import datetime, timedelta

FREE_PLAN_LIMIT = 10000
STARTER_PLAN_LIMIT = 100000
PAID_PLAN_LIMIT = 500000

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def create_user(session: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password).decode('utf-8')
    db_user = User(email=user.email, password_hash=hashed_password, name=user.name)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    default_project = UserProject(name=user.project_name, user_id=db_user.id, is_default=True)
    session.add(default_project)
    session.commit()

    return db_user


def get_user_by_email(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()


def reset_request_count_if_needed(user: User):
    now = datetime.now()
    if now.month != user.last_request_reset.month or now.year != user.last_request_reset.year:
        # user.request_count = 0
        user.last_request_reset = now

def increment_request_count(user: User, db: Session):
    reset_request_count_if_needed(user)
    # if user.subscription_plan == "free" and user.request_count >= FREE_PLAN_LIMIT:
    #     raise HTTPException(status_code=403, detail="Request limit exceeded for free plan")
    # elif user.subscription_plan == "paid" and user.request_count >= PAID_PLAN_LIMIT:
    #     raise HTTPException(status_code=403, detail="Request limit exceeded for paid plan")
    # user.request_count += 1
    db.add(user)
    db.commit()
    db.refresh(user)

def get_user_projects(db: Session, user_id: int):
    return db.exec(select(UserProject).where(UserProject.user_id == user_id)).all()

def save_user_project(db: Session, user_id: int, project_name: str):
    # Check if the user has reached the maximum number of projects
    existing_projects = db.query(UserProject).filter(UserProject.user_id == user_id).count()
    if existing_projects >= 10:
        raise HTTPException(status_code=400, detail="Maximum number of projects reached")
    
    project = UserProject(name=project_name, user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
