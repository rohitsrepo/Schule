from django.db import models
from django.conf import settings
from django.contrib import admin
from datetime import time
from courses.signals import CreateCourseMembership
from django.core.urlresolvers import reverse
# Create your models here.

def get_upload_file_name(instance,filename):
	return 'uploadedFiles/Courses/%s/%s_%s' % (instance.name, str(time()).replace('.','_'), filename)

def get_resource_file_name(instance,filename):
	return 'uploadedFiles/Courses/%s/resources/%s_%s' % (instance.course.name, str(time()).replace('.','_'), filename)


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
		if 'user' in kwargs.keys() and self.pk is None:
			sendSignal = True
			user = kwargs.pop('user',None)

		super(Course,self).save(*args,**kwargs)
		
		if sendSignal:
			CreateCourseMembership.send(sender =Course, instance =self, user =user, created=True)

	def __str__(self):
		return 'Course: '+self.name

	def get_absolute_url(self):
		return reverse('course_home', args=[str(self.id)])

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
	data = models.FileField(upload_to=get_resource_file_name)
	date =  models.DateTimeField(auto_now_add=True)
	course = models.ForeignKey(Course)
	
	def get_absolute_url(self):
		return reverse('course_resource_home', args=(course.id, self.id))

	def __str__(self):
		if len(self.title) > 12:
			return 'Resource: '+self.title[:12]+'...'
		return 'Resource: '+self.title

admin.site.register(CourseResource)

class Assignment(models.Model):
	title = models.CharField(max_length = 200)
	description = models.TextField()
	createdOn = models.DateTimeField(auto_now_add = True)
	createdBy = models.ForeignKey(settings.AUTH_USER_MODEL)
	submitOn = models.DateTimeField()

	def get_absolute_url(self):
		pass

	def __str__(self):
		if len(self.title) > 12:
			return 'Assignment: '+self.title[:12]+'...'
		return 'Assignment: '+self.title

admin.site.register(Assignment)

class AssignmentResources(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank = True)
	data = models.FileField(upload_to=get_upload_file_name)
	assignment = models.ForeignKey(Assignment)	

	def __str__(self):
		if len(self.title > 12):	
			return 'Assignment Resource: '+self.title[12]+'...'
		return 'Assignment Resource: '+self.title	

admin.site.register(AssignmentResources)
