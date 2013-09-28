from django.db import models
from django.conf import settings
from django.contrib import admin
from datetime import time
from courses.signals import CreateCourseMembership
# Create your models here.

def get_upload_file_name(instance,filename):
	return 'uploadedFiles/%s_%s' % (str(time()).replace('.','_'),filename)


class Course(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	startDate = models.DateField()
	endDate = models.DateField()
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CourseMembership")
	coursePhoto = models.FileField(blank=True, null=True, upload_to= get_upload_file_name)
	courseVideo = models.FileField(blank=True, null=True,upload_to = get_upload_file_name)
	
	def save(self,*args,**kwargs):
		sendSignal = False
		if 'user' in kwargs and self.pk is None:
			sendSignal = True

		super(Course,self).save(*args,**kwargs)
		
		if sendSignal:
			CreateCourseMemberShip.send(sender =Course,instance =self,user =kwargs['user'],created=True)

admin.site.register(Course)

class CourseMembership(models.Model):
	userTypeChoices=(
		('OW','Owner'),
		('ST','Student'),
		('MO','Moderator'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	course = models.ForeignKey(Course)
	userType = models.CharField(max_length = 10, choices = userTypeChoices)

class CourseResource(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank=True)
	data = models.FileField(upload_to=get_upload_file_name)
	course = models.ForeignKey(Course)

admin.site.register(CourseResource)

class Assignment(models.Model):
	title = models.CharField(max_length = 200)
	description = models.TextField()
	createdOn = models.DateTimeField(auto_now_add = True)
	createdBy = models.ForeignKey(settings.AUTH_USER_MODEL)
	submitOn = models.DateTimeField()

admin.site.register(Assignment)

class AssignmentResources(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank = True)
	data = models.FileField(upload_to=get_upload_file_name)
	assignment = models.ForeignKey(Assignment)	

admin.site.register(AssignmentResources)
