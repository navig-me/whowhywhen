from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.beat_schedule = {
    'check-monitors-every-5-minutes': {
        'task': 'app.tasks.check_all_monitors',
        'schedule': 300.0,
    },
}

celery_app.conf.timezone = 'UTC'
