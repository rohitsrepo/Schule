from django.db import models
from courses.models import Course
from groups.models import Group
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
# Create your models here.

def get_upload_file_name_courses(instance,filename):
	return 'uploadedFiles/Courses/%s/Polls/%s_%s' % (instance.course.name,str(time()).replace('.','_'),filename)


class CoursePoll(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	createDate = models.DateField(auto_now_add = True)
	course = models.ForeignKey(Course)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='creater+')
	voters = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='voter+')
	data = models.FileField(upload_to=get_upload_file_name_courses, blank=True)

class CoursePollOption(models.Model):
	name = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	poll = models.ForeignKey(CoursePoll)
'''
class CoursePollResource(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	data = models.FileField(upload_to= get_upload_file_name_course)
	poll = models.ForeignKey(CoursePoll)
'''

def get_upload_file_name_groups(instance,filename):
	return 'uploadedFiles/Groups/%s/Forums/%s_%s' % (instance.group.name, str(time()).replace('.','_'),filename)


class GroupPoll(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	createDate = models.DateField(auto_now_add = True)
	group = models.ForeignKey(Group)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='author+')
	voters = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='voters+')
	data = models.FileField(upload_to=get_upload_file_name_groups, blank=True)

class GroupPollOption(models.Model):
	name = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	poll = models.ForeignKey(GroupPoll)
'''
class GroupPollResource(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	data = models.FileField(upload_to= get_upload_file_name_group)
	poll = models.ForeignKey(GroupPoll)
'''

'''
class BasePoll(models.Model):
	content_type = models.ForeignKey(ContentType,verbose_name=('content type'))
	object_pk=models.TextField(verbose_name='object ID')
	content_object = generic.GenericForeignKey(ct_field="content_type",fk_field="object_pk")
	
	class Meta:
		abstract=True

class Poll(BasePoll):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	createDate = models.DateField(auto_now_add=True)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL)


class PollOption(models.Model):
	name = models.CharField(max_length=200)
	votes = models.IntegerField()
	poll = models.ForeignKey(Poll)
	voters = models.ManyToManyField(settings.AUTH_USER_MODEL)

class PollResource(models.Model):
	title = models.CharField(max_length =100)
	description = models.TextField(blank = True)
	data = models.FileField(upload_to=get_upload_file_name)
	coursePoll = models.ForeignKey(Poll)
'''
