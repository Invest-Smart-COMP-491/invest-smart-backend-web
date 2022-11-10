import re
from investsmart.scrape.crawl_reddit import RedditScraper

class Recommender:
    def __init__(self):
        pass

    @staticmethod
    def getTopPerformers(self):
        #TODO: get top performing stocks of the week

    def getRedditTrending(self):
        freq_dict = {}
        reddit = RedditScraper()
        posts = reddit.getPosts(subreddit="wallstreetbets", lim=30)
        
        for info in posts:
            stonk = re.findall(r'[A-Z]{3}(?<![A-Z]{4})(?![A-Z])', info['title'] + info['body'] + info['comments']))
            freq_dict[stonk] = freq_dict.get(stonk, 0) + 1
        
