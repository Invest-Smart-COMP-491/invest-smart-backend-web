import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from gnews import GNews
from htmldate import find_date
from dateutil import parser
import datetime
import pytz

scraped_dict = {}

class NewsScraper:
    def __init__(self, stock_name, stock_ticker):
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker
        self.news_functions = [self.getGoogleNews, self.getGoogleFinanceNews, self.getYahooNews]


    def CustomFindDate(self,url): # updated 
        date = None
        try:
            html = requests.get(url).content.decode('utf-8')
            date = find_date(html, outputformat='%Y-%m-%d %H:%M:%S')
        except:
            date = datetime.datetime.now(pytz.utc).strftime(format="%Y-%m-%d %H:%M:%S") # TODO: you can handle in different way  - format is same with above one 
        return date 

    

    def getAllNews(self):
        df_news = []

        for news_function in self.news_functions:
            try:
                df = news_function()
                #print(df)
                if not df.empty:
                    df_news.append(df)
            except Exception as e:
                print(e)
                print("Error for ", self.stock_name, " during calling ", news_function)
        
        results = pd.DataFrame()
        if len(df_news) > 0:
            results = pd.concat(df_news)
            results = results.drop_duplicates(subset='url').reset_index().drop(['index'], axis=1)
        return results

    def getGoogleFinanceNews(self):
        mapper = {"BRK-B": "BRK.A"}
        market = ":NASDAQ"

        if self.stock_ticker in mapper:
            market = ":NYSE"
            self.stock_ticker = mapper[self.stock_ticker]

        url = requests.get("https://www.google.com/finance/quote/" + self.stock_ticker + market)

        soup = BeautifulSoup(url.content, 'html.parser')
        soup = soup.find_all('div', attrs={'class': 'yY3Lee'})
        news = []
        for item in soup:
            url = item.find('a', attrs={'rel': 'noopener noreferrer'})['href']
            if url in scraped_dict:
                continue
            scraped_dict[url] = 'v'

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

        results['published_date'] = results['published_date'].apply(lambda x: parser.parse(x).replace(tzinfo=pytz.UTC)) 
        return results

    def getGoogleNews(self):
        google_news = GNews(max_results=20)

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
        
        results['published_date'] = results['published date'].apply(lambda x: parser.parse(x).replace(tzinfo=pytz.UTC)) 
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
        results['published_date'] = df['providerPublishTime'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).replace(tzinfo=pytz.UTC))
        results['url'] = df['link']
        results['publisher'] = df['publisher']
        results['href'] = df['link'].apply(lambda x: x.partition('.com')[0] + ".com")
        return results
