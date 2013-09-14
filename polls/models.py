from django.db import models
from courses.models import Course
from django.conf import settings
# Create your models here.

def get_upload_file_name(instance,filename):
	return 'uploadedFiles/%s_%s' % (str(time()).replace('.','_'),filename)

class CoursePoll(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	createDate = models.DateField(auto_now_add=True)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL)


class CoursePollOption(models.Model):
	name = models.CharField(max_length=200)
	votes = models.IntegerField()
	voters = models.ManyToManyField(settings.AUTH_USER_MODEL)

class CoursePollResource(models.Model):
	title = models.CharField(max_length =100)
	description = models.TextField(blank = True)
	data = models.FileField(upload_to=get_upload_file_name)
	coursePoll = models.ForeignKey(CoursePoll)
