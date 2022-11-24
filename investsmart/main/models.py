from django.db import models
from datetime import datetime
from django.utils import timezone
#from tinymce.models import HTMLField
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField #when migrating models to postgreSQL, we will implement arrayField
from django.urls import reverse

# Create your models here.

# if needed check - slugify 

class AssetCategory(models.Model):
	category_name = models.CharField(max_length = 200,unique=True)
	slug = models.SlugField(null=True)
	liked_count = models.IntegerField(default=0) # needed to handle 
	
	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name_plural = 'Categories'


class FavouriteCategory(models.Model):
	user = models.ForeignKey(CustomUser,default=None,verbose_name='User',on_delete=models.CASCADE)
	asset_category = models.ForeignKey(AssetCategory, default=None, verbose_name="Category", on_delete=models.SET_DEFAULT)
	favourite_date = models.DateTimeField("date added",default=timezone.now)
	
	def __str__(self):
		return self.user.username + ": " + self.asset_category.category_name

	class Meta:
		verbose_name_plural = 'FavouriteCategories'

class Asset(models.Model):
	asset_name = models.CharField(max_length = 200,default=None)
	asset_ticker = models.CharField(max_length = 20,unique=True)
	last_price = models.FloatField(default=0)
	asset_category = models.ForeignKey(AssetCategory, default=None, verbose_name="Category", on_delete=models.SET_DEFAULT)
	view_count = models.IntegerField(default=0)
	photo_link = models.URLField(null=True, blank=True) #URLField is needed or CharField is enough? 
	market_size = models.FloatField(default=0)
	liked_count = models.IntegerField(default=0) # needed to handle 

	def __str__(self):
		return self.asset_name

	class Meta:
		verbose_name_plural = 'Assets'

class FavouriteAsset(models.Model):
	user = models.ForeignKey(CustomUser,default=None,verbose_name='User',on_delete=models.CASCADE)
	asset = models.ForeignKey(Asset, default=None, verbose_name="Asset", on_delete=models.CASCADE)
	favourite_date = models.DateTimeField("date added",default=timezone.now)

	def __str__(self):
		return self.user__username + " " + self.asset__asset_ticker

	class Meta:
		verbose_name_plural = 'FavouriteAssets'

class AssetPrice(models.Model):
	asset = models.ForeignKey(Asset, default=None, verbose_name="Asset", on_delete=models.CASCADE)
	date_time = models.DateTimeField("price time",default=timezone.now)
	price = models.FloatField(default=0)
	volume = models.FloatField(default=0)

	def __str__(self):
		return self.asset.asset_ticker+ ": " + self.date_time.strftime("%Y-%m-%d, %H:%M:%S")

	class Meta:
		constraints = [
		models.UniqueConstraint(
			fields=['asset', 'date_time'], name='unique_asset_date'
			)
		]

		get_latest_by = "date_time"

		verbose_name_plural = 'AssetPrices'


class News(models.Model):
	title = models.CharField(max_length = 200,unique=True)
	description = models.TextField(null=True, blank=True)
	url = models.URLField(default=None) 
	published_date = models.DateTimeField("published date",default=timezone.now)
	publisher = models.CharField(max_length = 200)
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
	like_count = models.IntegerField(default=0) # needed to handle 
	imported_from = models.CharField(max_length = 200)

	def __str__(self):
		return self.comment_text

	class Meta:
		verbose_name_plural = 'Comments'

class CommentLike(models.Model): # TODO: dönerken tüm comment likelarını dönmemek için stock da tutabiliriz belki
	#yada commentlerin idler ile inner join atmak lazım
	user = models.ForeignKey(CustomUser,default=None,verbose_name='User',on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, default=None, verbose_name="Comment", on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username + ": " + self.comment.comment_id

	class Meta:
		verbose_name_plural = 'Commentlikes'
