import pandas as pd
import praw
client_id = 'Xa4qKcIg4UntujY4wOWnig'
secret = 'xsdo1Us0l79PSdTvCdp_Kx591LQwbA'
user_agent = 'invest'

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)  # TODO: anonimized version

    def getPosts(self, subreddit, lim=10):
        posts = []
        subreddit = self.reddit.subreddit(subreddit)

        for post in subreddit.hot(limit=lim):
            posts.append(
                [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext,
                 post.created])

        posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body',
                                             'created'])
        return posts

    def scrapeComments(self, post):
        submission = self.reddit.submission(url=post.url)

        comment_ls = list()
        for top_level_comment in submission.comments:
            try:
                comment_ls.append(top_level_comment.body)
            except:
                continue

        return comment_ls