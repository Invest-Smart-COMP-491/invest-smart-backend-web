from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages 
from .forms import NewUserForm,NewUserLoginForm

from django.contrib.auth.decorators import login_required

# Create your views here.

class RegisterView(View):
	template_name = "accounts/register.html"

	def get(self,request,*args,**kwargs):
		form = NewUserForm()
		return render(request = request,template_name = self.template_name,context={"form":form})

	def post(self, request, *args, **kwargs):
		form = NewUserForm(request.POST)

		if form.is_valid():
			user = form.save()
			first_name = form.cleaned_data.get('first_name')
			login(request, user)
			messages.success(request,f"Hello, {first_name}")
			return redirect('/')
		else:
			for msg in form.error_messages:
				messages.error(request,f"{msg}: {form.error_messages[msg]}")
			return render(request = request,template_name = self.template_name,context={"form":form}) 


class LoginView(View):
	template_name = "accounts/login.html"

	def get(self,request,*args,**kwargs):
		form = NewUserLoginForm()
		return render(request = request,template_name = self.template_name,context={"form":form})

	def post(self, request, *args, **kwargs):
		
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

		# form = NewUserLoginForm() # should we initialize credentials again? 

		return render(request = request,template_name = self.template_name,context={"form":form})


class LogoutView(View):

	def get(self,request,*args,**kwargs):
		logout(request)
		messages.info(request, "Logged out successfully!")
		return redirect("/")


	def post(self, request, *args, **kwargs):
		HttpResponse("Page Loaded")  

class ProfileView(View):
	template_name = "accounts/profile.html"

	def get(self,request,*args,**kwargs):
		user = request.user
		return render(request=request,template_name=self.template_name,context={"user":user})


	def post(self, request, *args, **kwargs):
		HttpResponse("Page Loaded") 

