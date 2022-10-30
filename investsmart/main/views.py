from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from .models import TestModel
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 

from django.contrib.auth.decorators import login_required



# Create your views here.


class HomeView(View):

	template_name = "main/home.html"

	def get(self,request,*args,**kwargs):
		return render(request=request,template_name=self.template_name,context={"testModel":TestModel.objects.all})

	def post(self, request, *args, **kwargs):
		return HttpResponse("Page Loaded") 

#def homepage(request):
#	#return HttpResponse("This is an <strong>InvestSmart</strong> HomePage.")
#	return 



