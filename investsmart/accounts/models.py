from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
	#public_name = models.CharField(max_length = 20,unique=True)

	public_name = models.CharField(max_length = 20,default=None, null=True)
    # add additional fields in here
    

	def __str__(self):
		return self.username
	
	def save(self, *args, **kwargs) :
		if not self.public_name:
			self.public_name = self.username
		super(CustomUser, self).save(*args, **kwargs)