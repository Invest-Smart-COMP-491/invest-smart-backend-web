from celery import shared_task
from datetime import datetime
from scrape.news_scraper import NewsScraper
from main import helper
import datetime


@shared_task(name="upload_news")
def upload_news(period, stock_name, stock_ticker, *args, **kwargs):
    nscraper = NewsScraper(stock_name, stock_ticker)
    df_news = nscraper.getAllNews(datetime.timedelta(hours=period))
    print(f"{df_news.shape[0]} news for {stock_ticker} scraped")
    helper.createandUpdateNews(stock_name, stock_ticker, df_news)


@shared_task(name="update_prices")
def update_prices(*args, **kwargs):
    helper.updateLastPricesAll()
    