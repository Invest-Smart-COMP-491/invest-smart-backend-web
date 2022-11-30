from django.contrib import admin
from .models import *
# from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.


"""
keep it if needed custom admin page 
class TestModelAdmin(admin.ModelAdmin):
	#fields = ["test_model_title","test_model_content","test_model_published"]
	#fields = ["test_model_title","test_model_published","test_model_content"]

	fieldsets = [("Title/Date",{"fields" : ["test_model_title","test_model_published"]}),
				("Content", {"fields" : ["test_model_content"]}),
				("Additional",{"fields": ["test_model_additional"]})]

	formfield_overrides = {
		models.TextField: {'widget':TinyMCE()}
	}

admin.site.register(TestModel,TestModelAdmin)
"""

admin.site.register(AssetCategory)
admin.site.register(Asset)
admin.site.register(News)
admin.site.register(AssetPrice)
admin.site.register(FavouriteAsset)
admin.site.register(FavouriteCategory)
admin.site.register(Comment)

