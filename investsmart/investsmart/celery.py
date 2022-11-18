import os
from celery import Celery
from scrape.constants import STOCK_TICKERS_LIST, STOCKS_LIST

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investsmart.settings')

celery_app = Celery('investsmart')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

for (stock_name, stock_ticker) in zip(STOCKS_LIST, STOCK_TICKERS_LIST):
    us_sched = {
        # Scheduler Name
        'update-news-'+stock_name: {
            # Task Name (Name Specified in Decorator)
            'task': 'upload_news',
            # Schedule
            'schedule': 3600.0,
            # Function Arguments
            'args': (2, stock_name, stock_ticker)
        },
    }
    # Python >= 3.5:
    celery_app.conf.beat_schedule = {**celery_app.conf.beat_schedule, **us_sched}
    # Python 3.9: 
    #celery_app.conf.beat_schedule |= us_sched
