from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import datetime

from accounts.models import SchuleUser

try:
	from django.utils import timezone
	now = timezone.now()
except ImportError:
	now = datetime.datetime.now 

class Incident(models.Model):
	actor_content_type = models.ForeignKey(ContentType, related_name='actor')
	actor_object_id = models.PositiveIntegerField()
	actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

	verb = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)

	target_content_type = models.ForeignKey(ContentType, related_name='target', blank=True, null=True)
	target_object_id = models.PositiveIntegerField(blank=True, null=True )
	target = generic.GenericForeignKey('target_content_type', 'target_object_id')

	action_object_content_type = models.ForeignKey(ContentType, related_name='action_object', blank=True, null=True)
	action_object_id = models.PositiveIntegerField(blank=True, null=True )
	action_object = generic.GenericForeignKey('action_object_content_type', 'action_object_id')

	created_at = models.DateTimeField(auto_now_add=True)
	targeted_at = models.DateTimeField(default = now)
	
	processed = models.BooleanField(default=False)
	public = models.BooleanField(default=True)
	
	class Meta:
		ordering=('-created_at',)

	def __unicode__(self):
	        ctx = {
	            'actor': self.actor,
	            'verb': self.verb,
	            'action_object': self.action_object,
	            'target': self.target,
	            'timesince': self.timesince()
	        }

	        if self.target:
	            if self.action_object:
	                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
	            return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx

	        if self.action_object:
	            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx

	        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

	def timesince(self, now=None):
		from django.utils.timesince import timesince as _
		return _(self.created_at,now)

	def mark_as_processed(self):
		self.processed =True
		self.save()




class Update(models.Model):
	incident = models.ForeignKey(Incident)
	
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType)
	recepient = generic.GenericForeignKey('content_type', 'object_id')

	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(default=now)
	public = models.BooleanField(default=False)
	onself = models.BooleanField(default=False)

	class Meta:
		ordering = ('-timestamp',)

	def mark_as_read(self):
		self.read =True
		self.save()

	def timesince(self, time_now=None):
		from django.utils.timesince import timesince as _
		return _(self.timestsamp,time_now)


class Follow(models.Model):
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	leader = generic.GenericForeignKey('content_type','object_id')
	followers = models.ManyToManyField(SchuleUser)

	class Meta:
		unique_together = ('content_type', 'object_id')
