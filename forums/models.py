from django.db import models
from courses.models import Course
from django.conf import settings
from datetime import time
# Create your models here.

def get_upload_file_name(instance,filename):
	return 'uploadedFiles/Courses/%s/Forums/%s_%s' % (instance.course.name,str(time()).replace('.','_'),filename)

class CourseForum(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	course =models.ForeignKey(Course)
	createDate = models.DateField(auto_now_add=True)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL)
	data = models.FileField(upload_to=get_upload_file_name,blank=True)

class CourseForumComment(models.Model):
	comment = models.TextField(max_length=200)
	commentDate = models.DateTimeField(auto_now_add=True)
	forum = models.ForeignKey(CourseForum)
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL)
'''
class CourseForumResource(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank= True)
	data = models.FileField(upload_to = get_upload_file_name)
	courseForum = models.ForeignKey(CourseForum)
'''
