from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import DetailView,ListView
from django.http import HttpResponse
from main import models
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 

from django.contrib.auth.decorators import login_required
from .helper import createandUpdateAssets,updateLastPrices,createandUpdateNews,updatePrices,getAssetPrice
from reco.stock_recommender import SimilarStocks, getPopularAssets

from api import serializers 
# Create your views here.

class HomeView(View):

	template_name = "main/index.html"

	def get(self,request,*args,**kwargs):
		
		top_n = 10 # top 10 news, can be reassigned 
		
		asset_ls = getPopularAssets()
		top_assets = models.Asset.objects.filter(asset_ticker__in = asset_ls)[:top_n]
		# TODO: after deploy to postgres, apply .distinct() to get distinct news from each asset; 
		
		#top_asset_news = models.News.objects.filter(asset__in=top_assets).order_by('-published_date')[:10]
		top_asset_news = models.News.objects.filter(asset__asset_ticker__in=asset_ls).order_by('-published_date')[:top_n]

		# you will get top ten news and assets(you can use for: .... top_asset.last_price)
		return render(request=request,template_name=self.template_name,context={"top_assets":top_assets,"top_news":top_asset_news})
		# return render(request=request,template_name=self.template_name,context={models.AssetCategory.objects.all})

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class updateAssetsView(View):
	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		createandUpdateAssets()
		messages.info(request, "Assets Updated successfully!")
		return redirect("main:homepage")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class updateNewsView(View):
	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		# createandUpdateNews() # as I understand it changed to automatically update - delete this view? 
		messages.info(request, "News will be updated automatically!")
		return redirect("main:homepage")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class updatePricesView(View):
	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		updatePrices()
		messages.info(request, "Prices Updated successfully!")
		return redirect("main:homepage")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class categoryView(View):
	template_name = "main/category_detail.html"

	def get(self,request,*args,**kwargs):
		slug = kwargs.get('slug')
		categories = [c.slug for c in models.AssetCategory.objects.all()]
		if slug in categories:
			asset_series = models.Asset.objects.filter(asset_category__slug=slug)
			return render(request,template_name=self.template_name,context={"category":slug,"asset_series": asset_series})

		return HttpResponse(f"{slug} does not correspond to anything.")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class AssetDetailView(View):
	model = models.Asset
	template_name = "main/asset_detail.html"

	def get(self,request,*args,**kwargs):
		if len(kwargs) > 0:
			slug = kwargs.get('slug')
			assets = [c.asset_ticker for c in models.Asset.objects.all()]
			if slug in assets:

				asset = models.Asset.objects.filter(asset_ticker=slug).first()
				asset.view_count += 1 
				asset.save()
				all_news = models.News.objects.filter(asset=asset)
				assetPrices = getAssetPrice(slug)  # do not save to the database directly gets from api 
				assetPrices = serializers.AssetPriceSerializer(assetPrices, many=True)
				return render(request,template_name=self.template_name,context={"asset": asset, "all_news":all_news,"asset_prices":assetPrices})
		else:
			all_assets = models.Asset.objects.all()
			return render(request,template_name=self.template_name,context={"asset": all_assets}) #can be handled in in HTML 
		
		return HttpResponse(f"{slug} does not correspond to anything.")

	def post(self, request, *args, **kwargs):

		if request.POST["action"] == "favouriteAsset":
			response_data = {}
			asset_ticker = request.POST.get("asset_ticker")
			asset = models.Asset.objects.filter(asset_ticker=asset_ticker).first()
			user = request.user
			favouriteAssetObj = models.FavouriteAsset.objects.get_or_create(user=user,asset=asset)
			asset.save()
		elif request.POST["action"] == "unfavouriteAsset":
			response_data = {}
			asset_ticker = request.POST.get("asset_ticker")
			asset = models.Asset.objects.filter(asset_ticker=asset_ticker).first()
			user = request.user
			models.FavouriteAsset.objects.filter(user=user,asset=asset).delete()
			asset.save()
		elif request.POST["action"] == "likeComment":
			response_data = {}
			comment_id = request.POST.get("comment_id")
			comment = models.Comment.objects.filter(id=comment_id).first()
			user = request.user
			comment.liked_users.add(user)
			comment.save()
		elif request.POST["action"] == "unlikeComment":
			response_data = {}
			comment_id = request.POST.get("comment_id")
			comment = models.Comment.objects.filter(id=comment_id).first()
			user = request.user
			comment.liked_users.remove(user)
			comment.save()
		elif request.POST["action"] == "favouriteAssetCategory": # TODO: can be moved/copy to the category view if needed 
			response_data = {}
			asset_category_slug = request.POST.get("asset_category_slug")
			assetCategory = models.AssetCategory.objects.filter(slug=asset_category_slug).first()
			user = request.user
			favouriteCategoryObj = models.FavouriteCategory.objects.get_or_create(user=user,asset_category=assetCategory)
			assetCategory.save()
		elif request.POST["action"] == "unfavouriteAssetCategory":
			response_data = {}
			asset_category_slug = request.POST.get("asset_category_slug")
			assetCategory = models.AssetCategory.objects.filter(slug=asset_category_slug).first()
			user = request.user
			models.FavouriFavouriteCategoryteAsset.objects.filter(user=user,asset_category=assetCategory).delete()
			assetCategory.save()








		return HttpResponse("Page Loaded") #TODO: json will be returned 

class AssetNewsView(View):
	model = models.Asset
	template_name = "main/asset_news.html"


	def get(self,request,*args,**kwargs):
		if len(kwargs) > 0:
			slug = kwargs.get('slug')
			assets = [c.asset_ticker for c in models.Asset.objects.all()]
			if slug in assets:
				asset = models.Asset.objects.filter(asset_ticker=slug).first()
				all_news = models.News.objects.filter(asset=asset)
				return render(request,template_name=self.template_name,context={"all_news":all_news,"asset": asset})
		else:
			all_news = models.News.objects.all()
			asset = None
			return render(request,template_name=self.template_name,context={"all_news":all_news,"asset": asset}) # asset empty 
		return HttpResponse(f"{slug} does not correspond to anything.")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class CurrentUserFavouriteAssetsView(View): #TODO:serializers
	def get(self, request, *args, **kwargs):

		user = request.user
		fav = models.FavouriteAsset.objects.filter(user=user)
		serializer = serializers.FavouriteAssetSerializer(fav, many=True)
		return render(request,template_name=self.template_name,context={"favourite_assets":serializer})

class CurrentUserFavouriteCategoryView(View):
	def get(self, request, *args, **kwargs):
		user = request.user
		ret = models.FavouriteCategory.objects.filter(user=user)
		serializer = serializers.FavouriteCategorySerializer(ret, many=True)
		return render(request,template_name=self.template_name,context={"favourite_categories":serializer})

class AssetPriceView(View):
	def get(self, request, *args, **kwargs):
		if len(kwargs) > 0:
			slug = kwargs.get('slug')
			assets = [c.asset_ticker for c in models.Asset.objects.all()]
			if slug in assets:
				#asset = models.Asset.objects.filter(asset_ticker=slug).first()
				#ret = models.AssetPrice.objects.filter(asset=asset)
				assetPrices = getAssetPrice(slug)  # do not save to the database directly gets from api 
				serializer = serializers.AssetPriceSerializer(assetPrices, many=True)
				return render(request,template_name=self.template_name,context={"prices":serializer}) # returns an object
		else:
			assets = models.Asset.objects.all() 
			serializer = serializers.AllAssetPriceSerializer(assets, many=True) #only last prices of assets ,
			return render(request,template_name=self.template_name,context={"prices":serializer}) # returns object list
		return HttpResponse(f"{slug} does not correspond to anything.")




