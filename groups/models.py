from django.db import models
from django.conf import settings
from django.contrib import admin
from datetime import time
from groups.signals import CreateGroupMembership
# Create your models here.

def get_upload_file_name(instance,filename):
        return 'uploadedFiles/Groups/%s/%s_%s' % (instance.name, str(time()).replace('.','_'), filename)

def get_resource_file_name(instance,filename):
        return 'uploadedFiles/Groups/%s/resources/%s_%s' % (instance.group.name, str(time()).replace('.','_'), filename)


class Group(models.Model):
        name = models.CharField(max_length=50)
        description = models.TextField()
        startDate = models.DateField()
        members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="GroupMembership")
        groupPhoto = models.FileField(blank=True, null=True, upload_to= get_upload_file_name)
        groupVideo = models.FileField(blank=True, null=True,upload_to = get_upload_file_name)

        def save(self,*args,**kwargs):
                sendSignal = False
                if 'user' in kwargs.keys() and self.pk is None:
                        sendSignal = True
                        user = kwargs.pop('user',None)

                super(Group,self).save(*args,**kwargs)

                if sendSignal:
                        CreateGroupMembership.send(sender =Group, instance =self, user =user, created=True)

admin.site.register(Group)

class GroupMembership(models.Model):
        userTypeChoices=(
                ('OW','Owner'),
                ('MM','Member'),
                ('MO','Moderator'),
        )
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        group = models.ForeignKey(Group)
        userType = models.CharField(max_length = 10, choices = userTypeChoices)

class GroupResource(models.Model):
        title = models.CharField(max_length = 100)
        description = models.TextField(blank=True)
        data = models.FileField(upload_to=get_resource_file_name)
        date =  models.DateTimeField(auto_now_add=True)
        group = models.ForeignKey(Group)

admin.site.register(GroupResource)
'''
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
'''
