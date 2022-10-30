from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
#from django.contrib.auth.models import User

from .models import CustomUser

class NewUserForm(UserCreationForm):
	email = forms.EmailField(
		label="Email",
		max_length=100,
		required = True,
		#help_text='Enter Email Address',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		)
	first_name = forms.CharField(
		label="First Name",
		max_length=100,
		required = True,
		#help_text='Enter First Name',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
		)
	last_name = forms.CharField(
		label="Last Name",
		max_length=100,
		required = True,
		#help_text='Enter Last Name',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
		)
	username = forms.CharField(
		label="User Name",
		max_length=200,
		required = True,
		#help_text='Enter Username',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
		)

	#username = forms.EmailField(
	#	label="Email",
	#	max_length=100,
	#	required = True,
	#	#help_text='Enter Email Address',
	#	widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
	#	)
	password1 = forms.CharField(
		label="Password",
		#help_text='Enter Password',
		required = True,
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
		)
	password2 = forms.CharField(
		label="Password Again",
		required = True,
		#help_text='Enter Password Again',
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
		)
	# check = forms.BooleanField(required = True)

	class Meta:
		model = CustomUser 
		#fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

		def save(self, commit=True):
			user = super(NewUserForm, self).save(commit=False)
			user.email = self.cleaned_data["email"]
			if commit:
				user.save()
			return user 


class NewUserLoginForm(AuthenticationForm):

	#username = forms.EmailField(
	#	label="Email",
	#	max_length=100,
	#	required = True,
	#	#help_text='Enter Email Address',
	#	widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
	#	)
	#password = forms.CharField(
	#	label="Password",
	#	#help_text='Enter Password',
	#	required = True,
	#	widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
	#	)



	class Meta:
		model = CustomUser 
		fields = ("username", "password")


class NewUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ("username", "email")


