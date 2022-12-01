import re
import pandas as pd
from scrape.crawl_reddit import RedditScraper
from scrape.constants import STOCK_TICKERS_LIST
from main.models import News

class Recommender:
    def __init__(self):
        pass

    def getTopPerformers(self) -> list:
        """Sorts dict by the popularity."""
        dc = {k.upper(): v for k, v in sorted(self.getRedditTrending().items(), key=lambda item: item[1])}
        #print(list(dc))
        return list(dc)

    def getRedditTrending(self) -> dict:
        freq_dict = {}
        reddit = RedditScraper()

        posts = reddit.getPosts(subreddit="wallstreetbets", lim=500)
        posts2 = reddit.getPosts(subreddit="stocks", lim=500)

        posts = pd.concat([posts, posts2])

        for row in posts[['title', 'body']].to_dict():
            stonk = re.findall(r'[A-Z]{3}(?<![A-Z]{4})(?![A-Z])',
                               (str([posts['title'].iloc[i] for i in range(len(posts['title']))])).replace("\\",
                                                                                                           "").replace(
                                   "'", ""))  # + info['comments']
            stonk2 = re.findall(r'[A-Z]{3}(?<![A-Z]{4})(?![A-Z])',
                                (str([posts['title'].iloc[i] for i in range(len(posts['body']))])).replace("\\",
                                                                                                           "").replace(
                                    "'", ""))  # + info['comments']


            for stock in stonk:
                if stock in STOCK_TICKERS_LIST:
                    freq_dict[stock] = freq_dict.get(stock, 0) + 1

            for stock in stonk2:
                if stock in STOCK_TICKERS_LIST:
                    freq_dict[stock] = freq_dict.get(stock, 0) + 1

        return freq_dict

class SimilarStocks:
    def __init__(self):
        self.reco_dict = {}

    """def getSimilars(self, ticker):
        news = News.objects.filter(asset=ticker)
        
        nes."""

    def buildSimilarityDict(self):
        #news = News.objects.all()
        #news = news[['asset', 'mentioned_asset']]
        df = pd.DataFrame(list(News.objects.all().values('asset', 'mentioned_asset')))
        reco_dict = {}
        for main_asset, mentioned_asset in df.iterrows():
            ls = reco_dict.get(main_asset, [])
            if mentioned_asset not in ls:
                reco_dict.get(main_asset, []).append(mentioned_asset)

        self.reco_dict = reco_dict

        #print(News.objects.all().values('asset', 'mentioned_asset'))

    def getSimilarAssets(self, asset):
        return self.reco_dict[asset]


def getPopularAssets():
    rec = Recommender()
    rec.getRedditTrending()
    return rec.getTopPerformers()



