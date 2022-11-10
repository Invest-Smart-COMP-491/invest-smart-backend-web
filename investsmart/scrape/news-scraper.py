import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from gnews import GNews
from htmldate import find_date
from dateutil import parser
import datetime


class NewsScraper:
    def __init__(self, stock_name, stock_ticker):
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker

    def getGoogleFinanceNews(self):
        url = requests.get("https://www.google.com/finance/quote/" + self.stock_ticker + ":NASDAQ")
        soup = BeautifulSoup(url.content, 'html.parser')
        soup = soup.find_all('div', attrs={'class': 'yY3Lee'})
        news = []
        for item in soup:
            url = item.find('a', attrs={'rel': 'noopener noreferrer'})['href']
            s_new = {
                "title": item.find('div', attrs={'class': 'Yfwt5'}).text,
                "published date": find_date(url),  # item.find('div', attrs={'class': 'Adak'}).text,
                "url": url,
                "publisher": item.find('div', attrs={'class': 'sfyJob'}).text,
                "href": url.partition('.com')[0] + ".com"

            }
            news.append(s_new)
        results = pd.DataFrame().from_dict(news)
        results['published date'] = results['published date'].apply(lambda x: parser.parse(x))
        return results

    def getNews(self):
        google_news = GNews()
        # google_news.period = '7d'
        news = google_news.get_news(self.stock_name)
        results = pd.DataFrame().from_dict(news)
        publisher = list(results['publisher'].to_dict().values())
        publisher = pd.DataFrame().from_dict(publisher)
        href = publisher['href']
        publisher_title = publisher['title']
        results.drop(['publisher'], axis=1)
        results['href'] = href
        results['publisher'] = publisher_title
        results['published date'] = results['published date'].apply(lambda x: parser.parse(x))
        return results

    def getYahooNews(self):
        stock = yf.Ticker(self.stock_ticker)
        df = pd.DataFrame().from_dict(stock.get_news())

        results = pd.DataFrame()
        results['title'] = df['title']
        results['published date'] = df['providerPublishTime'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        results['url'] = df['link']
        results['publisher'] = df['publisher']
        results['href'] = df['link'].apply(lambda x: x.partition('.com')[0] + ".com")
        return results


