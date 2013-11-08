from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser

# Create your models here.

class SchuleUser(AbstractUser):
	userType = models.CharField(max_length =10)

	# Split as Town, state, country, postal code etc.
	addressLine1 = models.CharField(max_length =100,blank =True)
	addressLine2 = models.CharField(max_length =100,blank =True)
	district  = models.CharField(max_length =20,blank =True)
	state = models.CharField(max_length =20,blank =True)
	country = models.CharField(max_length="20", default = "India",blank = True)
	postalCode = models.CharField(max_length = 12,blank = True)
	# Not really sure if this format is generic
	countryCode = models.CharField(max_length = 6,default = '+91',blank = True)
	phone = models.CharField(max_length =10,blank = True)
	birthDate = models.DateField(null = True,blank = True)
	registrationDate = models.DateField(auto_now=True, auto_now_add= True,blank = True)
	# Length chosen on estimate
	vigilanceKey = models.CharField(max_length=8)
	
	class Meta:
		app_label = "accounts"

#admin.site.register(SchuleUser)
