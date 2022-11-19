import numpy as np
import pandas as pd
import yfinance as yf
import finviz
from newspaper import Article
# from newsapi import NewsApiClient # gets error ? 
# ImportError: cannot import name 'NewsApiClient' from 'newsapi'
from scrape.api_keys import NEWS_API_KEY
from scrape.constants import STOCK_TICKERS_LIST

from datetime import datetime
from dateutil.relativedelta import relativedelta


def scrape(url):
    article = Article(url)
    article.download()
    article.parse()
    # nltk.download('punkt')  # 1 time download of the sentence tokenizer
    article.nlp()
    return article


class LivePrice:
    def __init__(self, stock_name):
        self.stock_name = stock_name

    def getLastPrice(self):
        data = yf.download(tickers=self.stock_name, period='1m', interval='1m')
        return data['Open'].iloc[-1]

    def getPrice(self,period="2y",interval="1h",start=datetime.now()-relativedelta(years=2),end=datetime.now()):
        data = yf.download(tickers=self.stock_name, start=start,end=end, interval=interval)[['Open', 'Volume']]
        data = data.reset_index().rename(columns = {'index':'date_time'})
        return data

    def getCompanyInfo(self):
        stock = yf.Ticker(self.stock_name)
        info_dict = stock.info

        dc = {k: v for k, v in info_dict.items() if k in ['sector', 'shortName', 'logo_url', 'marketCap', 'industry']}
        return dc

    def getTarget(self):
        return finviz.get_analyst_price_targets(self.stock_name)

    def getNews(self): # yahoo finance
        stock = yf.Ticker(self.stock_name)
        self.stock = stock
        return self.stock.news


class DBUpdater():
    def __init__(self):
        pass

    def updateAllLastPrices(self):
        map(self.updateLastPrice, STOCK_TICKERS_LIST)

        """for st in STOCKS_LIST:
            lp = LivePrice(st)
            last_price = lp.getLastPrice()
            self.updateLastPrice(st, last_price)"""

    def updateLastPrice(self, ticker):
        lp = LivePrice(ticker)
        last_price = lp.getLastPrice()
        db.update(ticker, last_price)

    def updateAllAnalystTargets(self):
        map(self.updateAnalystTargets, STOCK_TICKERS_LIST)

    def updateAnalystTargets(self, ticker):
        lp = LivePrice(ticker)
        targets = lp.getLastPrice()

        """{'date': '2022-10-28',
         'category': 'Reiterated',
         'analyst': 'Wedbush',
         'rating': 'Outperform',
         'target_from': 220.0,
         'target_to': 200.0}"""
        for tar in targets:
            db.update(tar)


class NewsAPI:
    def __init__(self):
        self.client = NewsApiClient(api_key=NEWS_API_KEY)
        sources = self.client.get_sources()
        eng_ls = [i for i in sources['sources'] if i['language'] == 'en']
        self.eng_sources_str = str([j['id'] for j in eng_ls]).replace('[', '').replace(']', '').replace('\'', '')

    def getBusinessNews(self):
        return self.client.get_top_headlines(category="business", sources=self.eng_sources_str)

    def getAllNews(self, query):
        news_list = self.client.get_everything(q=query, from_param='2022-10-10', to='2022-11-09')
        return news_list