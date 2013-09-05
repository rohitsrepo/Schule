from django.db import models
from djnago.contrib.auth.models import User
# Create your models here.

'''
class Course(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	start_date = models.DateField()
	end_date = models.DateField()
	members = models.ManyToManyField(User, through="CourseMembership")


class CourseMembership(models.Model):
	user = models.ForeignKey(User)
	course = models.ForeignKey(Course)
	user_type = models.
'''
