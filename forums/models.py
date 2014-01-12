from django.db import models
from courses.models import Course
from groups.models import Group
from django.conf import settings
from datetime import time
from django.core.urlresolvers import reverse
# Create your models here.

def get_upload_file_name_courses(instance,filename):
	return 'uploadedFiles/Courses/%s/Forums/%s_%s' % (instance.course.name,str(time()).replace('.','_'),filename)

class CourseForum(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	course =models.ForeignKey(Course)
	createDate = models.DateField(auto_now_add=True)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL)
	data = models.FileField(upload_to=get_upload_file_name_courses,blank=True)

	def __str__(self):
		if len(self.title) > 12:
			return 'Forum: '+self.title[:12]+'...'
		return 'Forum: '+self.title

	def get_absolute_url(self):
		return reverse('course_forumHome', args=[self.course.id, self.id])



class CourseForumComment(models.Model):
	comment = models.TextField(max_length=200)
	commentDate = models.DateTimeField(auto_now_add=True)
	forum = models.ForeignKey(CourseForum)
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __str__(self):
		if len(self.comment) > 12:
			return 'Comment: '+self.comment[:12]+'...'
		return 'Comment: '+self.comment

	def get_absolute_url(self):
		return reverse('course_forumHome', args=[forum.course.id, forum.id])

'''
class CourseForumResource(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank= True)
	data = models.FileField(upload_to = get_upload_file_name)
	courseForum = models.ForeignKey(CourseForum)

'''
def get_upload_file_name_groups(instance,filename):
	return 'uploadedFiles/Groups/%s/Forums/%s_%s' % (instance.group.name,str(time()).replace('.','_'),filename)

class GroupForum(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	group =models.ForeignKey(Group)
	createDate = models.DateField(auto_now_add=True)
	creater = models.ForeignKey(settings.AUTH_USER_MODEL)
	data = models.FileField(upload_to=get_upload_file_name_groups,blank=True)

	def __str__(self):
		if len(self.title) > 12:
			return 'Forum: '+self.title[:12]+'...'
		return 'Forum: '+self.title

	def get_absolute_url(self):
		return reverse('group_forumHome', args=[self.group.id, self.id])

class GroupForumComment(models.Model):
	comment = models.TextField(max_length=200)
	commentDate = models.DateTimeField(auto_now_add=True)
	forum = models.ForeignKey(GroupForum)
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __str__(self):
		if len(self.title) > 12:
			return 'Forum: '+self.title[:12]+'...'
		return 'Forum: '+self.title

	def get_absolute_url(self):
		return reverse('group_forumHome', args=[forum.group.id, forum.id])


'''
class CourseForumResource(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank= True)
	data = models.FileField(upload_to = get_upload_file_name)
	courseForum = models.ForeignKey(CourseForum)
'''
