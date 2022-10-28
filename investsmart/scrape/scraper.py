import numpy as np
import pandas as pd
import yfinance as yf


from investsmart.scrape.constants import STOCK_TICKERS_LIST


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
