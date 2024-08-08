
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models.user import UserPushSubscription
from app.schemas.user import PushSubscriptionCreate
from fastapi import APIRouter, Depends, HTTPException


from app.crud.user import create_user_alert_config
from app.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserAlertConfigCreate, UserAlertConfigRead
from app.services.monitoring_service import fetch_user_alert_config_notifications

router = APIRouter()

@router.post("/alerts/config", response_model=UserAlertConfigRead)
def save_user_alert_config(
    alert_config: UserAlertConfigCreate, 
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    return create_user_alert_config(session, current_user.id, alert_config)

@router.get("/alerts")
def get_user_alert_configs(
    current_user: User = Depends(get_current_user), 
    page: int = 1,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    alert_results, total = fetch_user_alert_config_notifications(session, current_user.id, page, limit)
    return {
        "results": alert_results,
        "total": total
    }


@router.post("/subscribe-push")
def subscribe_push(subscription: PushSubscriptionCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Check if user_id and endpoint already exist in the database
    user_push_subscription = session.query(UserPushSubscription).filter(UserPushSubscription.user_id == current_user.id, UserPushSubscription.endpoint == subscription.endpoint).first()
    if user_push_subscription:
        if user_push_subscription.p256dh != subscription.keys.p256dh or user_push_subscription.auth != subscription.keys.auth:
            user_push_subscription.p256dh = subscription.keys.p256dh
            user_push_subscription.auth = subscription.keys.auth
            session.add(user_push_subscription)
            session.commit()

        return {"message": "Subscription updated successfully"}
    
    push_subscription = UserPushSubscription(
        user_id=current_user.id,
        endpoint=subscription.endpoint,
        p256dh=subscription.keys.p256dh,
        auth=subscription.keys.auth
    )
    session.add(push_subscription)
    session.commit()
    return {"message": "Subscription added successfully"}
