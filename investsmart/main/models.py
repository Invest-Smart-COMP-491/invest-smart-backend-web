from django.db import models
from datetime import datetime
from django.utils import timezone
from tinymce.models import HTMLField

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


"""
class NewsModel(models.Model):
	title = models.CharField(max_length = 200)
	url = models.TextField()
	tag = [models.CharField]
	date = models.DateTimeField("date published", default=timezone.now)

	def __str__(self):
		return self.test_model_title
"""
