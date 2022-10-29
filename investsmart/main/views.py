from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import TestModel

# Create your views here.


def homepage(request):
	#return HttpResponse("This is an <strong>InvestSmart</strong> HomePage.")
	return render(request=request,template_name="main/home.html",context={"testModel":TestModel.objects.all})
