import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from investsmart.scrape.constants import STOCK_TICKERS_LIST, STOCKS_LIST

tfidf_vectorizer = TfidfVectorizer(analyzer="char")

#sparse_matrix = tfidf_vectorizer.fit_transform([string]+string_list)
#cosine = cosine_similarity(sparse_matrix[0,:],sparse_matrix[1:,:])

class SearchRecommender:
    def __init__(self):
        self.initTickers()
        self.initDB()

    def initTickers(self):
        self.tickers = [i.lower() for i in STOCK_TICKERS_LIST]

    def initDB(self):
        self.db = [i.lower() for i in STOCKS_LIST]

    def query(self, search_str):
        print('query:', search_str)
        closest_res_name = difflib.get_close_matches(search_str, self.db, cutoff=.5)
        closest_res_tk = difflib.get_close_matches(search_str, self.tickers, cutoff=.5)
        print("diff:", closest_res_name)
        print("diff ticker:", closest_res_tk)
        return closest_res_name + closest_res_tk

        """tfidf_vectorizer = TfidfVectorizer(analyzer="char")

        sparse_matrix = tfidf_vectorizer.fit_transform([search_str] + self.db)
        cosine = cosine_similarity(sparse_matrix[0, :], sparse_matrix[1:, :])
        print("cos:", STOCK_TICKERS_LIST[np.argmax(cosine)], np.max(cosine))

        sparse_matrix = tfidf_vectorizer.fit_transform([search_str] + self.tickers)
        cosine = cosine_similarity(sparse_matrix[0, :], sparse_matrix[1:, :])

        print("cos ticker:", STOCK_TICKERS_LIST[np.argmax(cosine)], np.max(cosine))"""