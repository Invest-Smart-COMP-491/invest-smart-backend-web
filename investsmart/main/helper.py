import os
from scrape.constants import STOCK_TICKERS_LIST,STOCKS_LIST
#import sys
#sys.path.append('../scrape')
from scrape.scraper import LivePrice
from scrape.news_scraper import NewsScraper
from .models import AssetCategory,Asset,News

def createandUpdateAssets():
	for ticker,name in zip(STOCK_TICKERS_LIST,STOCKS_LIST):

		if "." in ticker: #.B ones have problem - we will handle it later 
			continue


		try:
			asset = Asset.objects.get(asset_ticker = ticker)
		except asset.DoesNotExist:
			asset = createandUpdateAsset(ticker,name)

		updateLastPrice(ticker)


def createandUpdateAsset(ticker,name):

	lp = LivePrice(ticker)
	company_info = lp.getCompanyInfo()

	if company_info==None or company_info["marketCap"]==None:
		CatObj, created  = AssetCategory.objects.get_or_create(category_name="No Category",slug="No-Category")
		logo_url = None
		market_cap = 0
	else:
		# some tickers have None info
		CatObj, created = AssetCategory.objects.get_or_create(category_name=company_info["sector"],slug=company_info["sector"].replace(" ","-"))
		logo_url = company_info["logo_url"]
		market_cap = company_info["marketCap"]

	asset = Asset(asset_ticker = ticker,asset_name = name ,asset_category = CatObj ,photo_link = logo_url , market_size =  market_cap)
	asset.save()

	return asset




def updateLastPrices():
	map(updateLastPrice, STOCK_TICKERS_LIST)


def updateLastPrice(ticker):
	asset = Asset.objects.get(asset_ticker=ticker)
	lp = LivePrice(ticker)
	try:
		last_price = lp.getLastPrice()
		asset.last_price = last_price
		asset.save()
	except:
		print(ticker," failed to update price")
		
def createandUpdateNews():
	for ticker,name in zip(STOCK_TICKERS_LIST,STOCKS_LIST):

		if "." in ticker: #.B ones have problem - we will handle it later 
			continue

		try:
			asset = Asset.objects.get(asset_ticker = ticker)
		except asset.DoesNotExist:
			asset = createandUpdateAsset(ticker,name)

		downloadNews(ticker,name,asset)

def downloadNews(ticker,name,asset):

	n_scraper = NewsScraper(name,ticker)
	results = n_scraper.getAllNews()

	"""This method is depreciated due to long run time, TODO: update db directly from dataframe"""

	# Not able to iterate directly over the DataFrame
	df_records = results.to_dict()

	model_instances = [News(
	    title=df_records['title'][record],
	    description = df_records['description'][record],
	    url = df_records['url'][record],
	    published_date = df_records['published_date'][record],
	    publisher =  df_records['publisher'][record],
	    asset = asset
	) for record in range(len(df_records["title"]))]

	News.objects.bulk_create(model_instances,ignore_conflicts = True) # update_conflicts=True

	"""
	for news in results:
		try:

			newsDB = News.objects.get(title = news["title"])
			print(newsDB)
		except news.DoesNotExist:
			newsDB = News(title = news["title"],description = news['description'] ,href = news['href'] ,published_date = news['published_date'] , publisher =  news['publisher'],asset = asset)
			newsDB.save()

	"""
