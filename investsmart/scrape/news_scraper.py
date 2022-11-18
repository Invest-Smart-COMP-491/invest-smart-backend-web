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


    def CustomFindDate(self,url): # updated 
        date = None
        try:
            date = find_date(url)
        except:
            date = datetime.datetime.now().date().strftime(format="%Y-%m-%d") # TODO: you can handle in different way  - format is same with above one 
        return date 

    def getAllNews(self):
        gnews = self.getGoogleNews() # TODO: some returns empty,should handle it
        gfnews = self.getGoogleFinanceNews() # TODO: some returns empty,should handle it
        ynews = self.getYahooNews() # TODO: some returns empty,should handle it
        results = pd.concat([gnews, gfnews, ynews])
        results = results.drop_duplicates(subset='url').reset_index().drop(['index'], axis=1)
        return results

    def getGoogleFinanceNews(self):
        url = requests.get("https://www.google.com/finance/quote/" + self.stock_ticker + ":NASDAQ") 
        soup = BeautifulSoup(url.content, 'html.parser')
        soup = soup.find_all('div', attrs={'class': 'yY3Lee'})
        news = []
        for item in soup:
            url = item.find('a', attrs={'rel': 'noopener noreferrer'})['href']
            s_new = {
                "title": item.find('div', attrs={'class': 'Yfwt5'}).text,
                "description": "",
                "published_date": self.CustomFindDate(url),  # item.find('div', attrs={'class': 'Adak'}).text, # updated 
                "url": url,
                "publisher": item.find('div', attrs={'class': 'sfyJob'}).text,
                "href": url.partition('.com')[0] + ".com"

            }
            news.append(s_new)
        results = pd.DataFrame().from_dict(news)
        # updated 
        if results.empty: # TODO: handle empty results, I have handled direcly returning null, check it 
            return results

        results['published_date'] = results['published_date'].apply(lambda x: parser.parse(x)) 
        return results

    def getGoogleNews(self):
        google_news = GNews()
        # google_news.period = '7d'
        try:
            news = google_news.get_news(self.stock_name)
        except Exception as e:
            print(e)
            print("Error fetching news with google news stock: ", self.stock_name)
            return None

        results = pd.DataFrame().from_dict(news)
        publisher = list(results['publisher'].to_dict().values())
        publisher = pd.DataFrame().from_dict(publisher)
        href = publisher['href']
        publisher_title = publisher['title']
        results.drop(['publisher'], axis=1)
        results['href'] = href
        results['publisher'] = publisher_title
        
        results['published_date'] = results['published date'].apply(lambda x: parser.parse(x)) 
        results.drop(['published date'], axis=1, inplace=True)
        return results

    def getYahooNews(self):
        stock = yf.Ticker(self.stock_ticker)
        try:
            df = pd.DataFrame().from_dict(stock.get_news())
        except Exception as e:
            print(e)
            print("Error fetching news with Yahoo news: ", self.stock_ticker)
            return None

        results = pd.DataFrame()
        results['title'] = df['title']
        results['description'] = ""
        results['published_date'] = df['providerPublishTime'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        results['url'] = df['link']
        results['publisher'] = df['publisher']
        results['href'] = df['link'].apply(lambda x: x.partition('.com')[0] + ".com")
        return results
