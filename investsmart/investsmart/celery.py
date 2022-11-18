import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investsmart.settings')

celery_app = Celery('investsmart')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    # Scheduler Name
    'update-news': {
        # Task Name (Name Specified in Decorator)
        'task': 'upload_news',
        # Schedule
        'schedule': 300.0,
        # Function Arguments
        'args': (2,)
    },
}
