import re
import pandas as pd
from investsmart.scrape.crawl_reddit import RedditScraper
from investsmart.scrape.constants import STOCK_TICKERS_LIST


class Recommender:
    def __init__(self):
        pass

    @staticmethod
    def getTopPerformers(self):
        # TODO: get top performing stocks of the week
        return 0

    def getRedditTrending(self) -> dict:
        freq_dict = {}
        reddit = RedditScraper()

        posts = reddit.getPosts(subreddit="wallstreetbets", lim=500)
        posts2 = reddit.getPosts(subreddit="stocks", lim=500)

        posts = pd.concat([posts, posts2])
        # return posts
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