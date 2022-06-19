from celery import Celery

from app import settings

celery_app = Celery(
    "celery",
    backend=settings.celery_backend_db,
    broker=settings.celery_broker
)

celery_app.autodiscover_tasks(
    [
        "app.users"
    ]
)
