if __name__ == "__main__":
    subscription_info = {
        "endpoint": "https://fcm.googleapis.com/fcm/send/fJbvA4Syowg:APA91bFcXVvpv7B14w5i8ojYleZSlJYp1asFRl_RHgje8EIO7vS3PlNApEATtVJwH1UCZdVLpDKaDdPEBzotnt4VffK-Iej24XfB_UIbywrEP1YozeTJCpXoNyviKVigqJMz7cOpMQDM",
        "keys": {
            "p256dh": "BJksy7EJakUhHk_YXPziS3KaInvBY5OhuMMYDTlaa6IZWf5VjG0522OHkRavJK850inbBz9XnnJstv61A4F5BbY",
            "auth": "sHfuvzFvQJ3OUJfgl0vuAw"
        }
    }

    from app.services.monitoring_service import send_push_notification
    send_push_notification(subscription_info, "test message")
