from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta, datetime
import bcrypt
from typing import Optional
from jose import jwt
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.database import get_session
from app.crud.user import create_user, get_user_by_email, User, save_user_project, get_user_projects, verify_turnstile_token
from app.schemas.user import UserCreate, UserRead, UserStatusRead
from app.dependencies.auth import get_current_user
from app.models.user import User, UserProject, SubscriptionPlan
from app.models.apilog import APILog
from app.dependencies.auth import verify_password
from app.config import TURNSTILE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
import stripe
from app.crud.user import FREE_PLAN_LIMIT, STARTER_PLAN_LIMIT, PAID_PLAN_LIMIT

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter()

@router.get("/stripe/payment-link/{plan_name}", response_model=str)
def get_stripe_payment_link(current_user: User = Depends(get_current_user), plan_name: SubscriptionPlan = SubscriptionPlan.starter, session: Session = Depends(get_session)):
    if plan_name == SubscriptionPlan.free:
        return None
    elif plan_name == SubscriptionPlan.starter:
        price_id = 'price_1PaBdIC0V9GgAoCfI9gq9MSL'
    elif plan_name == SubscriptionPlan.pro:
        price_id = 'price_1PaBfwC0V9GgAoCfzrHuBtZs'

    # Return subscription link with price_id
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://whowhywhen.com/',
        customer_email=str(current_user.email),
        allow_promotion_codes=True,
    )
    return checkout_session.url
    
def get_user_subscription_from_stripe(current_user: User):
    user_email = current_user.email
    customers = stripe.Customer.list(email=user_email).data
    
    if not customers:
        return SubscriptionPlan.free
    
    print("Stripe customer found:", customers[0])

    customer_id = customers[0].id
    subscriptions = stripe.Subscription.list(customer=customer_id).data

    print("Subscriptions:", subscriptions)

    for subscription in subscriptions:
        if subscription.status == 'active':
            print("Subscription item:", subscription.plan)
            if subscription.plan.id == 'price_1PaBdIC0V9GgAoCfI9gq9MSL':
                return SubscriptionPlan.starter
            elif subscription.plan.id == 'price_1PaBfwC0V9GgAoCfzrHuBtZs':
                return SubscriptionPlan.pro
    return SubscriptionPlan.free
        
def refresh_user_subscription(current_user: User, session: Session = Depends(get_session)):
    user_subscription_plan = current_user.subscription_plan
    stripe_subscription = get_user_subscription_from_stripe(current_user)
    if user_subscription_plan != stripe_subscription:
        # Update user's subscription plan in the database, update monthly limit, and credit reset date
        current_user.subscription_plan = stripe_subscription
        if current_user.subscription_plan == SubscriptionPlan.free:
            current_user.monthly_credit_limit = FREE_PLAN_LIMIT
        elif current_user.subscription_plan == SubscriptionPlan.starter:
            current_user.monthly_credit_limit = STARTER_PLAN_LIMIT
        elif current_user.subscription_plan == SubscriptionPlan.pro:
            current_user.monthly_credit_limit = PAID_PLAN_LIMIT
        current_user.monthly_credit_usage_crossed = False
        session.add(current_user)
        session.commit()
        

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Verify the Turnstile token
    verify_turnstile_token(user.cf_turnstile_response, TURNSTILE_SECRET_KEY)

    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(session, user)

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_email(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/users/me", response_model=UserStatusRead)
def read_users_me(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    refresh_user_subscription(current_user, session)
    user_projects = get_user_projects(session,current_user.id)
    user_request_count = 0
    for project in user_projects:
        user_request_count += session.query(APILog).filter(APILog.user_project_id == project.id).filter(APILog.created_at >= current_user.monthly_credit_limit_reset).count()
    return {
        "user": current_user,
        "user_request_count": user_request_count
    }

@router.post("/users/me/projects")
def create_user_project(project_name: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return save_user_project(session, current_user.id, project_name)

@router.get("/users/me/projects")
def read_user_projects(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_user_projects(session, current_user.id)
    