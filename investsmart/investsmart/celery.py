import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investsmart.settings')

celery_app = Celery('investsmart')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    # Scheduler Name
    'print-message-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'print_msg_main',
        # Schedule
        'schedule': 10.0,
        # Function Arguments
        'args': ("Hello",)
    },
    # Scheduler Name
    'print-time-twenty-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'print_time',
        # Schedule
        'schedule': 20.0,
    },
    # Scheduler Name
    'calculate-forty-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'get_calculation',
        # Schedule
        'schedule': 40.0,
        # Function Arguments
        'args': (10, 20)
    },
}
