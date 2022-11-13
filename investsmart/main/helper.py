import os
from scrape.constants import STOCK_TICKERS_LIST,STOCKS_LIST
#import sys
#sys.path.append('../scrape')
from scrape.scraper import LivePrice
from .models import AssetCategory,Asset

def createandUpdateAssets():
	for ticker,name in zip(STOCK_TICKERS_LIST,STOCKS_LIST):

		if "." in ticker: #.B ones have problem - we will handle it later 
			continue


		try:
		    asset = Asset.objects.get(asset_ticker = ticker)
		except asset.DoesNotExist:

			lp = LivePrice(ticker)
			company_info = lp.getCompanyInfo()
			print(ticker)

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


		updateLastPrice(ticker)


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
		




