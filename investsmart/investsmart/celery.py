import os
from celery import Celery
from scrape.constants import STOCK_TICKERS_LIST, STOCKS_LIST

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investsmart.settings')

celery_app = Celery('investsmart')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

for (stock_name, stock_ticker) in zip(STOCKS_LIST, STOCK_TICKERS_LIST):
    us_sched = {
        'update-news-'+stock_name: {
            'task': 'upload_news',
            'schedule': 3600.0,
            'args': (2, stock_name, stock_ticker)
        },
    }
    celery_app.conf.beat_schedule = {**celery_app.conf.beat_schedule, **us_sched}

us_sched = {
    'update_prices': {
        'task': 'update_prices',
        'schedule': 120.0,
        'args': ()
    },
}

celery_app.conf.beat_schedule = {**celery_app.conf.beat_schedule, **us_sched}



# Python >= 3.5:
#celery_app.conf.beat_schedule = {**celery_app.conf.beat_schedule, **us_sched}
# Python 3.9: 
#celery_app.conf.beat_schedule |= us_sched
