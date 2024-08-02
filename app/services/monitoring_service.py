from datetime import datetime, timedelta

from sqlalchemy import select

from app.models.apilog import APILog
from app.models.user import (UserAlertConfig, UserAlertNotification,
                             UserAlertNotificationEmail)


def check_services(alert_config, session):
    last_checked = alert_config.last_checked
    check_interval = alert_config.check_interval
    
    # Calculate the time threshold for the interval
    time_threshold = datetime.now() - timedelta(minutes=check_interval)
    
    # Check if the last check was more than check_interval minutes ago OR if the last check is None
    if last_checked is None or (datetime.now() - last_checked).total_seconds() / 60 > check_interval:
        # Check for server errors
        if server_error_threshold := alert_config.server_error_threshold:
            server_error_count = session.query(APILog).filter(
                APILog.response_code.between(500, 599),
                APILog.created_at >= time_threshold
            ).count()
            print(f"Server error count: {server_error_count} for threshold: {server_error_threshold}")

            if server_error_count > server_error_threshold:
                # Create a notification
                notification = UserAlertNotification(
                    user_id=alert_config.user_id,
                    description=f"Server errors detected: {server_error_count} errors in the last {check_interval} minutes",
                    server_error_threshold=alert_config.server_error_threshold,
                    server_error_threshold_actual=server_error_count,
                    check_interval=check_interval,
                    created=datetime.now()
                )
                session.add(notification)
                session.commit()

        # Check for client errors
        client_error_threshold = alert_config.client_error_threshold
        if client_error_threshold:
            client_error_count = session.query(APILog).filter(
                APILog.response_code.between(400, 499),
                APILog.created_at >= time_threshold
            ).count()
            print(f"Client error count: {client_error_count} for threshold: {client_error_threshold}")
            
            if client_error_count > client_error_threshold:
                # Create a notification
                notification = UserAlertNotification(
                    user_id=alert_config.user_id,
                    description=f"Client errors detected: {client_error_count} errors in the last {check_interval} minutes",
                    client_error_threshold=alert_config.client_error_threshold,
                    client_error_threshold_actual=client_error_count,
                    check_interval=check_interval,
                    created=datetime.now()
                )
                session.add(notification)
                session.commit()

        # Check for slow responses
        slow_threshold = alert_config.slow_threshold
        if slow_threshold:
            slow_threshold_threshold = alert_config.slow_threshold_threshold
            slow_threshold_actual = session.query(APILog).filter(
                APILog.response_time > slow_threshold / 1000,
                APILog.created_at >= time_threshold
            ).count()

            print(f"Slow response count: {slow_threshold_actual} for threshold: {slow_threshold_threshold} (> {slow_threshold} ms)")
            
            if slow_threshold_actual > slow_threshold_threshold:
                # Create a notification
                notification = UserAlertNotification(
                    user_id=alert_config.user_id,
                    description=f"Slowness detected: {slow_threshold_actual} APIs with a response time more than {slow_threshold} ms in the last {check_interval} minutes",
                    slow_threshold=alert_config.slow_threshold,
                    slow_threshold_threshold=alert_config.slow_threshold_threshold,
                    slow_threshold_threshold_actual=slow_threshold_actual,
                    check_interval=check_interval,
                    created=datetime.now()
                )
                session.add(notification)
                session.commit()

        alert_config.last_checked = datetime.now()
        session.add(alert_config)
        session.commit()

def fetch_user_alert_configs(session, user_id, page, limit):
    offset = (page - 1) * limit
    configs = session.exec(select(UserAlertConfig).where(UserAlertConfig.user_id == user_id)).offset(offset).limit(limit).all()
    total = session.exec(select(UserAlertConfig).where(UserAlertConfig.user_id == user_id)).count()
    configs_results = []
    for config in configs:
        configs_results.append(config.dict())
        config.read_at = datetime.now()
        session.commit()

    return configs_results, total
