import os
from scrape.constants import STOCK_TICKERS_LIST,STOCKS_LIST
#import sys
#sys.path.append('../scrape')
from scrape.scraper import LivePrice, tickerPrices
from scrape.news_scraper import NewsScraper
from .models import AssetCategory,Asset,News,AssetPrice
import numpy as np 
from datetime import datetime
from dateutil.relativedelta import relativedelta

def createandUpdateAssets():
	for ticker,name in zip(STOCK_TICKERS_LIST,STOCKS_LIST):

		if "." in ticker: #.B ones have problem - we will handle it later 
			continue

		try:
			asset = Asset.objects.get(asset_ticker = ticker)
		except asset.DoesNotExist:
			asset = createandUpdateAsset(ticker,name)

		updateLastPrice(ticker)
		#updatePrice(ticker)


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

	asset = updateLastPrice(ticker)
	# updatePrice(ticker)

	return asset

def updatePrices(): # it does nothing for now - will be deleted - no database object for assetPrice 
	#for ticker in STOCK_TICKERS_LIST:
	pass
		#updatePrice(ticker)
	#map(updatePrice, STOCK_TICKERS_LIST)

def getAssetPrice(ticker):
	asset = checkTickerExist(ticker)
	lp = LivePrice(ticker)
	price_df = lp.getPrice(interval="1h",start=datetime.now()-relativedelta(years=1),end=datetime.now()) #this is 1 year - can change it
	model_instances = [AssetPrice(
		asset = asset,
		date_time=row['date_time'].tz_localize(tz='UTC'), #TODO: changing local time info to the UTC 
		price = row['Open'],
		volume = row['Volume'],
		) for index, row in price_df.iterrows()]

	return model_instances


def updatePrice(ticker):

	asset = checkTickerExist(ticker)

	assetPrices = AssetPrice.objects.filter(asset__asset_ticker = ticker).order_by("-date_time")
	if assetPrices.exists(): # there is no asset price data
		assetPriceLastDateTime = assetPrices[0].date_time # be careful: start last price  
	else:
		assetPriceLastDateTime = datetime.now() - relativedelta(years=1) # to get last 2 years prices 

	updateLastPrice(ticker)

	try:
		lp = LivePrice(ticker)
		price_df = lp.getPrice(start=assetPriceLastDateTime,end=datetime.now())

		model_instances = [AssetPrice(
			asset = asset,
		    date_time=row['date_time'].tz_localize(tz='UTC'), #TODO: changing local time info to the UTC 
		    price = row['Open'],
		    volume = row['Volume'],
		) for index, row in price_df.iterrows()]

		AssetPrice.objects.bulk_create(model_instances,ignore_conflicts = True) # update_conflicts=True
	except:
		print(ticker," failed to update price")


def updateLastPricesAll():
	df_prices = tickerPrices(STOCK_TICKERS_LIST)

	for ticker in STOCK_TICKERS_LIST:
		try:
			asset = Asset.objects.get(asset_ticker=ticker)
			last_price = df_prices[ticker]['Close'][-1]
			asset.last_price = last_price
			asset.save()
		except Exception as e:
			print(e)
			print(f"{ticker} failed to update price")



def updateLastPrices():
	map(updateLastPrice, STOCK_TICKERS_LIST)


def updateLastPrice(ticker):
	asset = checkTickerExist(ticker)
	lp = LivePrice(ticker)
	try:
		last_price = lp.getLastPrice()
		asset.last_price = last_price
		asset.save()
	except:
		print(ticker," failed to update price")

	return asset
		
def checkTickerExist(ticker):
	try:
		asset = Asset.objects.get(asset_ticker = ticker)
	except:
		asset = createandUpdateAsset(ticker,STOCKS_LIST[STOCK_TICKERS_LIST.index(ticker)])
	return asset

def createandUpdateNews(name, ticker, df_news):
	try:
		asset = checkTickerExist(ticker)

		model_instances = [News(
			title=row['title'],
			url = row['url'],
			published_date = row['published_date'],
			publisher =  row['publisher'],
			asset = asset,
			thumbnail = row['thumbnail'],
			summary = row['summary']
		) for index, row in df_news.iterrows()]

		News.objects.bulk_create(model_instances,ignore_conflicts = True) # update_conflicts=True
	except Exception as e:
			print(f"{ticker} failed to update news")
			print(e)