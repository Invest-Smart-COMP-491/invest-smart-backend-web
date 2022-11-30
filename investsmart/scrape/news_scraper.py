import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from gnews import GNews
from htmldate import find_date
from dateutil import parser
import datetime
import pytz
from newspaper import Article

scraped_dict = {}

class NewsScraper:
    def __init__(self, stock_name, stock_ticker):
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker
        self.news_functions = [self.getGoogleNews, self.getGoogleFinanceNews, self.getYahooNews]


    def CustomFindDate(self,url): 
        date = None
        try:
            html = requests.get(url).content.decode('utf-8')
            date = parser.parse(find_date(html, outputformat='%Y-%m-%d %H:%M:%S')).replace(tzinfo=pytz.UTC)
        except Exception as e:
            date = datetime.datetime.now(pytz.UTC) 
        return date 

    def scrape(self, url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return article
    

    def getAllNews(self, period):
        df_news = []

        for news_function in self.news_functions:
            try:
                df = news_function()
                if not df.empty:
                    df_news.append(df)
            except Exception as e:
                print(e)
                print(f"Error for {self.stock_name}, during calling {news_function} Exception: {e}")
        
        results = pd.DataFrame()
        if len(df_news) > 0:
            results = pd.concat(df_news)
            results = results.drop_duplicates(subset='url').reset_index().drop(['index'], axis=1)

        results = results[results['published_date'] >= datetime.datetime.now(pytz.utc) - period]
        results.reset_index(drop=True, inplace=True)

        for row in results.itertuples():
            try:
                article = self.scrape(row.url)
                if row.thumbnail is None or row.thumbnail == "":
                    results.at[row.Index, 'thumbnail'] = article.top_image

                results.at[row.Index, 'summary'] = article.summary
            except Exception as e:
                print(f"Couldn't scrape from {row.url}")

        return results

    def getGoogleFinanceNews(self):
        results = pd.DataFrame()
        try:
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
                    "summary": "",
                    "published_date": self.CustomFindDate(url),  # item.find('div', attrs={'class': 'Adak'}).text, # updated 
                    "url": url,
                    "publisher": item.find('div', attrs={'class': 'sfyJob'}).text,
                    "href": url.partition('.com')[0] + ".com",
                    "thumbnail": item.find('div', attrs={'class': 'nkXTJ'}).img['src']
                }
                news.append(s_new)
            results = pd.DataFrame().from_dict(news)
        except Exception as e:
            print(f"Error fetching news with Google Finance News: {self.stock_ticker}: {e}")
        return results

    def getGoogleNews(self):
        results = pd.DataFrame()
        google_news = GNews()
        try:
            news = google_news.get_news(self.stock_name)
            results = pd.DataFrame().from_dict(news)
            publisher = list(results['publisher'].to_dict().values())
            publisher = pd.DataFrame().from_dict(publisher)
            href = publisher['href']
            publisher_title = publisher['title']
            results.drop(['publisher'], axis=1)
            results['href'] = href
            results['publisher'] = publisher_title
            results['published_date'] = results['published date'].apply(lambda x: parser.parse(x).replace(tzinfo=pytz.UTC)) 
            results.drop(['published date', "description"], axis=1, inplace=True)
            results['thumbnail'] = ""
            results['summary'] = ""
            results['title'] = results['title'].apply(lambda x: x[:x.rfind(" - ")] if x.rfind(" - ")>0 else x)
        except Exception as e:
            print(f"Error fetching news with Google news: {self.stock_ticker}: {e}")
        
        return results

    def getYahooNews(self):
        results = pd.DataFrame()
        stock = yf.Ticker(self.stock_ticker)
        try:
            df = pd.DataFrame().from_dict(stock.get_news())
            results['title'] = df['title']
            results['summary'] = ""
            results['published_date'] = df['providerPublishTime'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).replace(tzinfo=pytz.UTC))
            results['url'] = df['link']
            results['publisher'] = df['publisher']
            results['href'] = df['link'].apply(lambda x: x.partition('.com')[0] + ".com")

            def getYahooThumbnailURL(x):
                df_n = pd.DataFrame().from_dict(x['resolutions'])
                df_n = df_n[df_n['tag'] == "original"]['url']
                if len(df_n) > 0:
                    return df_n[0]
                return ""
            results['thumbnail'] = df['thumbnail'].apply(lambda x: getYahooThumbnailURL(x) if type(x) is dict else "")
        except Exception as e:
            print(f"Error fetching news with Yahoo news: {self.stock_ticker}: {e}")
        return results

#For Testing       
"""
start = datetime.datetime.now()
df = NewsScraper("Apple", "AAPL").getAllNews(datetime.timedelta(hours=2))
end = datetime.datetime.now()
print(end-start)
print(df)
print(df.dtypes)
"""