from celery import shared_task
from datetime import datetime
from scrape.news_scraper import NewsScraper
from .helper import createandUpdateNews


#TODO: period is not used yet
@shared_task(name="upload_news")
def upload_news(period, stock_name, stock_ticker, *args, **kwargs):
    nscraper = NewsScraper(stock_name, stock_ticker)
    df_news = nscraper.getAllNews()
    createandUpdateNews(stock_name, stock_ticker, df_news)


