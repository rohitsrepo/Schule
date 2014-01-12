from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser

# Create your models here.

class SchuleUser(AbstractUser):
	userTypeChoices = (
		('ST','Student'),
		('IN','Instructor'),
		('MA','Manager'),
	)
	
	userType = models.CharField(max_length =2, choices = userTypeChoices, default = 'ST')

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
		permissions = (
			('create_edit_instructor',"Can create or edit instructors."),
			('create_edit_student',"Can create or edit students."),
			('create_edit_manager',"Can create or edit manager."),
		)

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

	def get_absolute_url(self):
		#TODO-Change is creating public user profile
		'''Return user full name to be used in updates.'''
		return ''
#admin.site.register(SchuleUser)
