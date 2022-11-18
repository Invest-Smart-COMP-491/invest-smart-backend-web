from celery import shared_task
from datetime import datetime
from scrape.constants import STOCK_TICKERS_LIST, STOCKS_LIST
from scrape.news_scraper import NewsScraper


#TODO: insert to db
#TODO: edit stocks
@shared_task(name="upload_news")
def upload_news(period, *args, **kwargs):
    #print("PERIOD: ", period, " TICKER:", len(STOCK_TICKERS_LIST)," STOCKS:", len(STOCKS_LIST))
    for i in range(len(STOCKS_LIST)):
        nscraper = NewsScraper(STOCKS_LIST[i], STOCK_TICKERS_LIST[i])
        news = nscraper.getAllNews()


