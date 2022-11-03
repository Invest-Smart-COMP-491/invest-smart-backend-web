import numpy as np
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from gnews import GNews
from newspaper import Article
import finviz

from investsmart.scrape.constants import STOCK_TICKERS_LIST


def scrape(url):
    article = Article(url)
    article.download()
    article.parse()
    # nltk.download('punkt')  # 1 time download of the sentence tokenizer
    article.nlp()
    return article


def getNews(stock_name):
    google_news = GNews()
    # google_news.period = '7d'
    return google_news.get_news(stock_name)


def getGoogleFinanceNews(stock_ticker):
    url = requests.get("https://www.google.com/finance/quote/" + stock_ticker + ":NASDAQ")
    soup = BeautifulSoup(url.content, 'html.parser')
    soup = soup.find_all('div', attrs={'class': 'yY3Lee'})
    news = []
    for item in soup:
        url = item.find('a', attrs={'rel': 'noopener noreferrer'})['href']
        new = {
            "title": item.find('div', attrs={'class': 'Yfwt5'}).text,
            "published date": item.find('div', attrs={'class': 'Adak'}).text,
            "url": url,
            "publisher": {'href': url.partition('.com')[0] + ".com",
                          'title': item.find('div', attrs={'class': 'sfyJob'}).text}
        }
        news.append(new)
    return news


class LivePrice:
    def __init__(self, stock_name):
        self.stock_name = stock_name

    def getLastPrice(self):
        data = yf.download(tickers=self.stock_name, period='1m', interval='1m')
        return data['Open'].iloc[-1]

    def getCompanyInfo(self):
        stock = yf.Ticker(self.stock_name)
        info_dict = stock.info

        dc = {k: v for k, v in info_dict.items() if k in ['sector', 'shortName', 'logo_url', 'marketCap', 'industry']}
        return dc

    def getTarget(self):
        return finviz.get_analyst_price_targets(self.stock_name)


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
