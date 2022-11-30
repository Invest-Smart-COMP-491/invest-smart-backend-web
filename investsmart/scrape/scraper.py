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


def tickerPrices(ticker_list):
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = ticker_list,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "ytd",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        #interval = "1m",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )
    return data


class LivePrice:
    def __init__(self, stock_name):
        self.stock_name = stock_name

    def getLastPrice(self):
        data = yf.download(tickers=self.stock_name, period='1m', interval='1m')
        return data['Open'].iloc[-1]

    def getPrice(self,period="2y",interval="1d",start=datetime.now()-relativedelta(years=1),end=datetime.now()):
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


class NewsAPI:
    def __init__(self):
        #self.client = NewsApiClient(api_key=NEWS_API_KEY)
        sources = self.client.get_sources()
        eng_ls = [i for i in sources['sources'] if i['language'] == 'en']
        self.eng_sources_str = str([j['id'] for j in eng_ls]).replace('[', '').replace(']', '').replace('\'', '')

    def getBusinessNews(self):
        return self.client.get_top_headlines(category="business", sources=self.eng_sources_str)

    def getAllNews(self, query):
        news_list = self.client.get_everything(q=query, from_param='2022-10-10', to='2022-11-09')
        return news_list