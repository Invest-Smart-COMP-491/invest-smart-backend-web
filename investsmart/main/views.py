from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import DetailView,ListView
from django.http import HttpResponse
from .models import TestModel,AssetCategory,Asset
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 

from django.contrib.auth.decorators import login_required
from .helper import createandUpdateAssets,updateLastPrices 


# Create your views here.


class HomeView(View):

	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		return render(request=request,template_name=self.template_name,context={"category":AssetCategory.objects.all})

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class updateAssetsView(View):
	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		createandUpdateAssets()
		return redirect("main:homepage")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class categoryView(View):
	template_name = "main/category_detail.html"

	def get(self,request,*args,**kwargs):
		slug = kwargs.get('slug')
		categories = [c.slug for c in AssetCategory.objects.all()]
		if slug in categories:
			asset_series = Asset.objects.filter(asset_category__slug=slug)
			return render(request,template_name=self.template_name,context={"asset_series": asset_series})

		return HttpResponse(f"{slug} does not correspond to anything.")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

class AssetDetailView(View):
	model = Asset
	template_name = "main/asset_detail.html"


	def get(self,request,*args,**kwargs):
		slug = kwargs.get('slug')
		assets = [c.asset_ticker for c in Asset.objects.all()]
		if slug in assets:
			asset = Asset.objects.filter(asset_ticker=slug).first()
			return render(request,template_name=self.template_name,context={"asset": asset})

		return HttpResponse(f"{slug} does not correspond to anything.")

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 


#def homepage(request):
#	#return HttpResponse("This is an <strong>InvestSmart</strong> HomePage.")
#	return 



