from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import DetailView,ListView
from django.http import HttpResponse
from main import models
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 

from django.contrib.auth.decorators import login_required
from .helper import createandUpdateAssets,updateLastPrices,createandUpdateNews,updatePrices

from api import serializers 
# Create your views here.

class HomeView(View):

	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		return render(request=request,template_name=self.template_name,context={"category":models.AssetCategory.objects.all})

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
				return render(request,template_name=self.template_name,context={"asset": asset})
		else:
			all_assets = models.Asset.objects.all()
			return render(request,template_name=self.template_name,context={"asset": all_assets}) #can be handled in in HTML 
		
		return HttpResponse(f"{slug} does not correspond to anything.")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

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

class AssetPriceView(View): #TODO:
	def get(self, request, *args, **kwargs):
		if len(kwargs) > 0:
			slug = kwargs.get('slug')
			assets = [c.asset_ticker for c in models.Asset.objects.all()]
			if slug in assets:
				asset = models.Asset.objects.filter(asset_ticker=slug).first()
				ret = models.AssetPrice.objects.filter(asset=asset)
				serializer = serializers.AssetPriceSerializer(ret, many=True)
				return render(request,template_name=self.template_name,context={"prices":serializer})
		else:
			assets = models.Asset.objects.all() 
			serializer = serializers.AllAssetPriceSerializer(assets, many=True) #only last prices of assets ,
			return render(request,template_name=self.template_name,context={"prices":prices})
        

		return Response(serializer.data, status=status.HTTP_200_OK)




