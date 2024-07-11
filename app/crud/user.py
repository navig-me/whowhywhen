from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user import User, UserProject
from app.schemas.user import UserCreate
import bcrypt
from datetime import datetime, timedelta
import requests
from app.services.stripe_service import create_stripe_customer, FREE_PLAN_LIMIT, STARTER_PLAN_LIMIT, PAID_PLAN_LIMIT
import uuid


def verify_turnstile_token(token: str, secret_key: str):
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    payload = {
        'secret': secret_key,
        'response': token
    }
    response = requests.post(url, data=payload)
    result = response.json()

    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Turnstile verification failed")

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def create_user(session: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password).decode('utf-8')
    db_user = User(email=user.email, password_hash=hashed_password, name=user.name)
    
    # Create a Stripe customer for the user
    try:
        stripe_customer_id = create_stripe_customer(name=db_user.name, email=db_user.email)
        db_user.stripe_customer_id = stripe_customer_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating Stripe customer: {str(e)}")

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    default_project = UserProject(name=user.project_name, user_id=db_user.id, is_default=True)
    session.add(default_project)
    session.commit()

    return db_user


def get_user_by_email(db: Session, email: str):
    print("Getting user by email...", email)
    return db.exec(select(User).where(User.email == email)).first() if email else None


def get_user_projects(db: Session, user_id: uuid.UUID):
    return db.exec(select(UserProject).where(UserProject.user_id == user_id)).all()

def save_user_project(db: Session, user_id: uuid.UUID, project_name: str):
    # Check if the user has reached the maximum number of projects
    existing_projects = db.query(UserProject).filter(UserProject.user_id == user_id).count()
    if existing_projects >= 10:
        raise HTTPException(status_code=400, detail="Maximum number of projects reached")
    
    project = UserProject(name=project_name, user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
