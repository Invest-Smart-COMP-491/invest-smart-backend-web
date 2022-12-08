from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
	public_name = models.CharField(max_length = 20,unique=True)
    # add additional fields in here
    

	def __str__(self):
		return self.username