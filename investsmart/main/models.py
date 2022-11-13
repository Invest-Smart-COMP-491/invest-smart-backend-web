from django.db import models
from datetime import datetime
from django.utils import timezone
from tinymce.models import HTMLField
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField # when migrating models to postgreSQL, we will implement arrayField
from django.urls import reverse

# Create your models here.
class TestModel(models.Model):
	test_model_title = models.CharField(max_length = 200)
	test_model_content = models.TextField()
	test_model_additional = HTMLField(default=None) # from tinymce 
	test_model_published = models.DateTimeField("date published",default=timezone.now)

	def __str__(self):
		return self.test_model_title

	class Meta:
		verbose_name_plural = 'TestModels'

# if needed check - slugify 

class AssetCategory(models.Model):
	category_name = models.CharField(max_length = 200,unique=True)
	slug = models.SlugField(null=True)

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name_plural = 'Categories'

	#def get_absolute_url(self):
	#	return reverse("category_detail", kwargs={"slug": self.slug})



class Asset(models.Model):
	asset_name = models.CharField(max_length = 200,default=None)
	asset_ticker = models.CharField(max_length = 20,unique=True)
	last_price = models.FloatField(default=0)
	asset_category = models.ForeignKey(AssetCategory, default=None, verbose_name="Category", on_delete=models.SET_DEFAULT)
	view_count = models.IntegerField(default=0)
	photo_link = models.URLField(null=True, blank=True) #URLField is needed or CharField is enough? 
	market_size = models.FloatField(default=0)

	def __str__(self):
		return self.asset_name

	class Meta:
		verbose_name_plural = 'Assets'


class News(models.Model):
	title = models.CharField(max_length = 200,unique=True)
	link = models.URLField(default=None) 
	date_time = models.DateTimeField("date published",default=timezone.now)
	source = models.CharField(max_length = 200)
	asset = models.ForeignKey(Asset, default=None, verbose_name="Asset", on_delete=models.SET_DEFAULT)
	#mentioned_asset = models.ManyToManyField(Asset)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'Newss'	

class Comment(models.Model):
	user = models.ForeignKey(CustomUser,default=None,verbose_name='User',on_delete=models.CASCADE)
	asset = models.ForeignKey(Asset, default=None, verbose_name="Asset", on_delete=models.CASCADE)
	comment_text = models.TextField()
	date_time = models.DateTimeField("date published",default=timezone.now)
	parent_comment = models.ForeignKey("self",on_delete=models.CASCADE) #cascading or keeping comment? 
	like_count = models.IntegerField(default=0)
	imported_from = models.CharField(max_length = 200)
	# liked_users = models.ManyToManyField(CustomUser)

	def __str__(self):
		return self.comment_text

	class Meta:
		verbose_name_plural = 'Comments'


class favourite(models.Model):
	user = models.ForeignKey(CustomUser,default=None,verbose_name='User',on_delete=models.CASCADE)
	asset = models.ForeignKey(Asset, default=None, verbose_name="Asset", on_delete=models.CASCADE)
	favourite_date = models.DateTimeField("date published",default=timezone.now)

	def __str__(self):
		return self.user__username + " " + self.asset__asset_ticker

	class Meta:
		verbose_name_plural = 'Favourites'


class CommentLike(models.Model):
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser,default=None,verbose_name='User',on_delete=models.SET_DEFAULT)

	def __str__(self):
		return self.user__username + " " + self.comment__comment_id

	class Meta:
		verbose_name_plural = 'Favourites'





"""
class NewsModel(models.Model):
	title = models.CharField(max_length = 200)
	url = models.TextField()
	tag = [models.CharField]
	date = models.DateTimeField("date published", default=timezone.now)

	def __str__(self):
		return self.test_model_title
"""
