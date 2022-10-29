from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from .models import TestModel
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 
from .forms import NewUserForm,NewUserLoginForm

# Create your views here.


def homepage(request):
	#return HttpResponse("This is an <strong>InvestSmart</strong> HomePage.")
	return render(request=request,template_name="main/home.html",context={"testModel":TestModel.objects.all})

def register(request):

	if request.method == "POST":
		form = NewUserForm(request.POST)

		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			login(request, user)
			messages.success(request,f"Hello, {username}")
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request,f"{msg}: {form.error_messages[msg]}")

	else : 
		form = NewUserForm()

	return render(request = request,template_name = "main/register.html",context={"form":form})

def login_request(request):
	if request.method == 'POST':
		form = NewUserLoginForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			email = form.cleaned_data.get('email')
			user = authenticate(username=username, password=password)

			# TODO: Change it to email authentication - email = username can be possible 
			#user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect('/')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	
	form = NewUserLoginForm()
	return render(request = request,
					template_name = "main/login.html",
					context={"form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("main:homepage")