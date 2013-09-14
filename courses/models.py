from django.db import models
from django.conf import settings
# Create your models here.

def get_upload_file_name(instance,filename):
	return 'uploadedFiles/%s_%s' % (str(time()).replace('.','_'),filename)


class Course(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	starDate = models.DateField()
	endDate = models.DateField()
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CourseMembership")
	coursePhoto = models.FileField(blank=True, null=True, upload_to= get_upload_file_name)
	courseVideo = models.FileField(blank=True, null=True,upload_to = get_upload_file_name)

class CourseMembership(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	course = models.ForeignKey(Course)
	userType = models.CharField(max_length = 10)

class CourseResource(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank=True)
	data = models.FileField(upload_to=get_upload_file_name)
	course = models.ForeignKey(Course)

class Assignment(models.Model):
	title = models.CharField(max_length = 200)
	description = models.TextField()
	createdOn = models.DateTimeField(auto_now_add = True)
	createdBy = models.ForeignKey(settings.AUTH_USER_MODEL)
	submitOn = models.DateTimeField()

class AssignmentResources(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank = True)
	data = models.FileField(upload_to=get_upload_file_name)
	assignment = models.ForeignKey(Assignment)	
