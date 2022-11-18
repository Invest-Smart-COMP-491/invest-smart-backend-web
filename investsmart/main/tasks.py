from celery import shared_task
from datetime import datetime
from scrape.news_scraper import NewsScraper


#TODO: insert to db
#TODO: edit stocks
@shared_task(name="upload_news")
def upload_news(period, stock_name, stock_ticker, *args, **kwargs):
    nscraper = NewsScraper(stock_name, stock_ticker)
    news = nscraper.getAllNews()
    #print(news)


