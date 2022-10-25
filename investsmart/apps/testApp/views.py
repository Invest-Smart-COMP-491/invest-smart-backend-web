# HttpResponse is used to
# pass the information
# back to view
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials

# set credential by(terminal): export GOOGLE_APPLICATION_CREDENTIALS="investsmart/invest-smart-8dcd2-firebase-adminsdk-db368-38fb52ea3f.json"
#cred = credentials.Certificate("invest-smart-8dcd2-firebase-adminsdk-db368-38fb52ea3f.json")
#database_app = firebase_admin.initialize_app(cred)
#database_app = firebase_admin.get_app(cred)


config = {
	"apiKey": "AIzaSyCsPLdMq1sD0W0LfJHvn2R3XmrWjSBVdpY",
	"authDomain": "invest-smart-8dcd2.firebaseapp.com",
	"projectId": "invest-smart-8dcd2",
	"databaseURL": "https://invest-smart-8dcd2-default-rtdb.firebaseio.com",
	"storageBucket": "invest-smart-8dcd2.appspot.com",
	#"messagingSenderId": "97595397493",
	#"appId": "1:97595397493:web:6acd5437d9fb9259ef6f3c",
	#"measurementId": "G-H2LRSGG6MQ",
	"serviceAccount": "invest-smart-8dcd2-firebase-adminsdk-db368-38fb52ea3f.json"
}

firebase = pyrebase.initialize_app(config)
#firebase = pyrebase.get_app(config)
db = firebase.database()



class TestLayout(View):
	templatename = "TestPanel/Test.html"

	def get(self,request,*args,**kwargs):
		data = {"name": "Firebase Test"}
		db.child("users").child("Morty").set(data)  # push
		userName = db.child("users").get().val()["Morty"]["name"]  # get
		return render(request, self.templatename, {"projectname": "userName"})

	def post(self, request, *args, **kwargs):
		return HttpResponse("I have done it")
