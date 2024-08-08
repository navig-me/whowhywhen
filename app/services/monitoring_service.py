from datetime import datetime, timedelta

from sqlalchemy import select

from app.models.apilog import APILog
from app.models.user import (UserAlertConfig, UserAlertNotification,
                             UserAlertNotificationEmail, UserProject)

from relative_datetime import DateTimeUtils

from app.config import VAPID_PRIVATE_KEY
from pywebpush import webpush, WebPushException
from fastapi import HTTPException
from app.models.user import UserPushSubscription
import traceback

def check_services(alert_config, session):
    last_checked = alert_config.last_checked
    check_interval = alert_config.check_interval
    
    time_threshold = datetime.now() - timedelta(minutes=check_interval)
    
    if last_checked is None or (datetime.now() - last_checked).total_seconds() / 60 > check_interval:
        server_error_threshold = alert_config.server_error_threshold
        if server_error_threshold:
            server_error_count = session.query(APILog).filter(
                APILog.response_code.between(500, 599),
                APILog.created_at >= time_threshold,
                APILog.user_project_id == alert_config.user_project_id
            ).count()
            print(f"Server error count: {server_error_count} for threshold: {server_error_threshold}")

            if server_error_count > server_error_threshold:
                notification = UserAlertNotification(
                    user_project_id=alert_config.user_project_id,
                    description=f"Server errors detected: {server_error_count} errors in the last {check_interval} minutes",
                    server_error_threshold=alert_config.server_error_threshold,
                    server_error_threshold_actual=server_error_count,
                    check_interval=check_interval,
                    created=datetime.now()
                )
                session.add(notification)
                user_project_id = alert_config.user_project_id
                user_project = session.query(UserProject).filter(UserProject.id == user_project_id).first()
                alert_message = f"{user_project.name}: {notification.description}"
                notify_new_alert(user_project.user_id, alert_message, session)
                
        client_error_threshold = alert_config.client_error_threshold
        if client_error_threshold:
            client_error_count = session.query(APILog).filter(
                APILog.response_code.between(400, 499),
                APILog.created_at >= time_threshold,
                APILog.user_project_id == alert_config.user_project_id
            ).count()
            print(f"Client error count: {client_error_count} for threshold: {client_error_threshold}")
            
            if client_error_count > client_error_threshold:
                notification = UserAlertNotification(
                    user_project_id=alert_config.user_project_id,
                    description=f"Client errors detected: {client_error_count} errors in the last {check_interval} minutes",
                    client_error_threshold=alert_config.client_error_threshold,
                    client_error_threshold_actual=client_error_count,
                    check_interval=check_interval,
                    created=datetime.now()
                )
                session.add(notification)
                user_project_id = alert_config.user_project_id
                user_project = session.query(UserProject).filter(UserProject.id == user_project_id).first()
                alert_message = f"{user_project.name}: {notification.description}"
                notify_new_alert(user_project.user_id, alert_message, session)
        
        slow_threshold = alert_config.slow_threshold
        if slow_threshold:
            slow_threshold_threshold = alert_config.slow_threshold_threshold
            slow_threshold_actual = session.query(APILog).filter(
                APILog.response_time > slow_threshold / 1000,
                APILog.created_at >= time_threshold,
                APILog.user_project_id == alert_config.user_project_id
            ).count()
            print(f"Slow response count: {slow_threshold_actual} for threshold: {slow_threshold_threshold} (> {slow_threshold} ms)")
            
            if slow_threshold_actual > slow_threshold_threshold:
                notification = UserAlertNotification(
                    user_project_id=alert_config.user_project_id,
                    description=f"Slowness detected: {slow_threshold_actual} APIs with a response time more than {slow_threshold} ms in the last {check_interval} minutes",
                    slow_threshold=alert_config.slow_threshold,
                    slow_threshold_threshold=alert_config.slow_threshold_threshold,
                    slow_threshold_threshold_actual=slow_threshold_actual,
                    check_interval=check_interval,
                    created=datetime.now()
                )
                session.add(notification)
                user_project_id = alert_config.user_project_id
                user_project = session.query(UserProject).filter(UserProject.id == user_project_id).first()
                alert_message = f"{user_project.name}: {notification.description}"
                notify_new_alert(user_project.user_id, alert_message, session)

        alert_config.last_checked = datetime.now()
        session.add(alert_config)
        session.commit()


# Call this function when a new alert is created
def notify_new_alert(user_id, alert_message, session):
    subscriptions = session.query(UserPushSubscription).filter_by(user_id=user_id).all()
    for subscription in subscriptions:
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth
            }
        }
        send_push_notification(subscription_info, alert_message)

def send_push_notification(subscription_info, message):
    try:
        print(webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:support@whowhywhen.com"}
        ))
    except WebPushException as ex:
        print(f"Push notification failed")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Push notification failed: {ex}")


def fetch_user_alert_config_notifications(session, user_id, page, limit):
    offset = (page - 1) * limit
    user_projects = session.query(UserProject).filter(UserProject.user_id == user_id).all()
    user_project_ids = [user_project.id for user_project in user_projects]
    print("Fetching user alert notifications for user", user_id, user_project_ids)
    user_alert_notifications = session.query(UserAlertNotification).filter(UserAlertNotification.user_project_id.in_(user_project_ids)).order_by(UserAlertNotification.created.desc()).offset(offset).limit(limit).all()
    notifications = []
    for user_notification in user_alert_notifications:
        user_project = session.query(UserProject).filter(UserProject.id == user_notification.user_project_id).first()
        relative_time, direction = DateTimeUtils.relative_datetime(user_notification.created)

        notifications.append({
            "id": user_notification.id,
            "user_project_id": user_notification.user_project_id,
            "user_project_name": user_project.name,
            "description": user_notification.description,
            "read_at": user_notification.read_at,
            "created": user_notification.created,
            "created_text": f"{relative_time} ago",
        })
        user_notification.read_at = datetime.now()
        session.commit()
    total = session.query(UserAlertNotification).filter(UserAlertNotification.user_project_id.in_(user_project_ids)).count()
    return notifications, total
