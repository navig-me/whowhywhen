from datetime import datetime, timedelta
from typing import Optional

import requests
import pyotp
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlmodel import Session

from app.config import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY,
                        TURNSTILE_SECRET_KEY)
from app.crud.user import (User, create_user, get_password_hash,
                           get_user_by_email, get_user_projects,
                           save_user_project, verify_turnstile_token)
from app.database import get_session
from app.dependencies.auth import get_current_user, verify_password
from app.models.apilog import APILog
from app.models.user import SubscriptionPlan, User, UserAlertNotification
from app.schemas.user import (ChangePasswordForm, UserCreate, UserRead, 
                              UserStatusRead)
from app.services.email_service import send_password_reset_email
from app.services.fa_service import (generate_totp_secret, generate_totp_uri,
                                     verify_totp_token)
from app.services.stripe_service import (get_customer_portal_url,
                                         get_payment_link,
                                         refresh_user_subscription)
from app.config import GOOGLE_CLIENT_ID, REDIRECT_URI, GOOGLE_CLIENT_SECRET

router = APIRouter()

@router.post("/google-login")
def google_login(id_token: str, db: Session = Depends(get_session)):
    print("Google login request")

    # Verify the id_token with Google
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid token")

    user_info = response.json()

    email = user_info["email"]
    user = get_user_by_email(db, email)

    new_user = False

    if not user:
        user_create = UserCreate(
            email=email,
            name=user_info["name"],
            password="google_oauth",  # Set a default password for Google users
        )
        user = create_user(db, user_create)
        new_user = True

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "new_user": new_user}


@router.get("/oauth2callback")
def callback(request: Request, db: Session = Depends(get_session)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    google_provider_cfg = requests.get("https://accounts.google.com/.well-known/openid-configuration").json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = requests.auth.oauth2.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.url_for("callback"),
        code=code,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    token_response_json = token_response.json()
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = requests.auth.oauth2.client.add_token(
        userinfo_endpoint, token=token_response_json["access_token"]
    )
    userinfo_response = requests.get(uri, headers=headers, data=body)

    user_info = userinfo_response.json()

    email = user_info["email"]
    user = get_user_by_email(db, email)

    if not user:
        user_create = UserCreate(
            email=email,
            name=user_info["name"],
            password="google_oauth",  # Set a default password for Google users
        )
        user = create_user(db, user_create)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/stripe/payment-link/{plan_name}", response_model=str)
def get_stripe_payment_link(current_user: User = Depends(get_current_user), plan_name: SubscriptionPlan = SubscriptionPlan.starter, session: Session = Depends(get_session)):
    return get_payment_link(current_user, plan_name, session)
    
@router.get("/stripe/customer-portal", response_model=str)
def get_customer_portal(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_customer_portal_url(current_user)

@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Verify the Turnstile token
    verify_turnstile_token(user.cf_turnstile_response, TURNSTILE_SECRET_KEY)

    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(session, user)

@router.post("/forgot-password")
def forgot_password(email: str, cf_turnstile_response: str, session: Session = Depends(get_session)):
    verify_turnstile_token(cf_turnstile_response, TURNSTILE_SECRET_KEY)

    user = get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")

    # Generate a temporary password
    temp_password = pyotp.random_base32()[:8]  # Generate an 8-character temporary password
    user.password_hash = get_password_hash(temp_password)
    
    session.add(user)
    session.commit()
    session.refresh(user)

    # Send the email with the temporary password
    send_password_reset_email(user.email, temp_password)
    
    return {"message": "Password reset email sent"}

@router.post("/change-password")
def change_password(form_data: ChangePasswordForm, current_user: User = Depends(get_current_user),  session: Session = Depends(get_session)):
    if not verify_password(form_data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    hashed_password = get_password_hash(form_data.new_password)
    current_user.password_hash = hashed_password
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_email(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.two_factor_enabled:
        return {"totp_required": True}

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-2fa")
def verify_2fa(user_email: str, token: str, session: Session = Depends(get_session)):
    user = get_user_by_email(session, user_email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    
    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(token):
        raise HTTPException(status_code=400, detail="Invalid 2FA token")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/get-2fa-qr-code")
def get_2fa_qr_code(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    totp_secret = generate_totp_secret()
    user.totp_secret = totp_secret
    session.add(user)
    session.commit()
    return {"totp_uri": generate_totp_uri(totp_secret, user.email, issuer_name="WhoWhyWhen")}

@router.post("/enable-2fa")
def enable_2fa(token: str = None, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if user.two_factor_enabled:
        raise HTTPException(status_code=400, detail="2FA is already enabled")

    # Validate current 2FA token
    if user.totp_secret and token:
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(token):
            raise HTTPException(status_code=400, detail="Invalid 2FA token")

    user.two_factor_enabled = True

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "2FA enabled successfully"}

@router.post("/disable-2fa")
def disable_2fa(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if not current_user.two_factor_enabled:
        raise HTTPException(status_code=400, detail="2FA is not enabled")

    current_user.totp_secret = None
    current_user.two_factor_enabled = False

    session.add(current_user)
    session.commit()

    return {"message": "2FA disabled successfully"}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/users/me", response_model=UserStatusRead)
def read_users_me(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    refresh_user_subscription(current_user, session)
    user_projects = get_user_projects(session, current_user.id)
    user_request_count = 0
    for project in user_projects:
        user_request_count += session.query(APILog).filter(APILog.user_project_id == project.id).filter(APILog.created_at >= current_user.monthly_credit_limit_reset).count()
    
    user_project_ids = [project.id for project in user_projects]
    unread_alert_count = session.query(UserAlertNotification).filter(UserAlertNotification.user_project_id.in_(user_project_ids)).filter(UserAlertNotification.read_at == None).count()
    
    return {
        "user": current_user,
        "user_request_count": user_request_count,
        "unread_alert_count": unread_alert_count
    }

@router.post("/users/me/projects")
def create_user_project(project_name: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return save_user_project(session, current_user.id, project_name)

@router.get("/users/me/projects")
def read_user_projects(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_user_projects(session, current_user.id)
