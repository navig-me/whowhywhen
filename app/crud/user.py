import uuid
from typing import List

import bcrypt
import pyotp
import requests
from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.user import User, UserAlertConfig, UserProject
from app.schemas.user import UserAlertConfigCreate, UserAlertConfigRead, UserCreate
from app.services.email_service import (
    send_new_user_notification_email,
    send_welcome_email,
)


def get_password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def create_user(session: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password).decode("utf-8")
    totp_secret = pyotp.random_base32()
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        totp_secret=totp_secret,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    if user.project_name:
        default_project = UserProject(
            name=user.project_name, user_id=db_user.id, is_default=True
        )
        session.add(default_project)
        session.commit()

    send_welcome_email(db_user.email, db_user.name)
    send_new_user_notification_email(db_user.email, db_user.name)

    return db_user


def get_user_by_email(db: Session, email: str):
    print("Getting user by email...", email)
    return db.exec(select(User).where(User.email == email)).first() if email else None


def get_user_projects(db: Session, user_id: uuid.UUID):
    return db.exec(select(UserProject).where(UserProject.user_id == user_id)).all()


def save_user_project(db: Session, user_id: uuid.UUID, project_name: str):
    # Check if the user has reached the maximum number of projects
    existing_projects = (
        db.query(UserProject).filter(UserProject.user_id == user_id).count()
    )
    if existing_projects >= 10:
        raise HTTPException(
            status_code=400, detail="Maximum number of projects reached"
        )

    project = UserProject(name=project_name, user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def create_user_alert_config(
    db: Session, user_id: uuid.UUID, alert_config: UserAlertConfigCreate
) -> UserAlertConfig:
    db_alert_config = UserAlertConfig(user_id=user_id, **alert_config.dict())
    db.add(db_alert_config)
    db.commit()
    db.refresh(db_alert_config)
    return db_alert_config


def get_user_alert_configs(db: Session, user_id: uuid.UUID) -> List[UserAlertConfig]:
    return db.exec(
        select(UserAlertConfig).where(UserAlertConfig.user_id == user_id)
    ).all()
