from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from .managers import IncidentManager, UpdateManager
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
	
	objects = IncidentManager()

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

	def to_html(self):
		'''Returns incident in form of string, directly usable in HTML. '''
		ctx = {
	            'actor': self._pad_html(self.actor),
	            'verb': self.verb,
	            'action_object':self._pad_html(self.action_object),
	            'target': self._pad_html(self.target),
	            'timesince': self.timesince()
	        }

	        if self.target:
	            if self.action_object:
	                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
	            return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx

	        if self.action_object:
	            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx

	        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

	def _pad_html(self, obj):
		#returns URL padded obj
		if obj:
			return '<a href="'+obj.get_absolute_url()+'">{0}</a>'.format(obj)
		return obj

	def timesince(self, now=None):
		from django.utils.timesince import timesince as _
		return _(self.created_at,now)

	def mark_as_processed(self):
		self.processed =True
		self.save()

	def create_update(self):
		'''Creates updates for user based on 
		   Follow table. '''	

		if self.target:
			try:
				target_follow = Follow.objects.get(object_id=self.target_object_id, content_type=self.target_content_type)
				#add update for target object ifit has followers.
				if target_follow.more_than_one_follow():
					target_object = self.target_content_type.get_object_for_this_type(id=self.target_object_id)
					Update.objects.create(incident= self, recepient=target_object, timestamp = self.created_at, onself=True)

				#Update the followers of this object.
				target_follow.update_followers(self)
		
			except Follow.Object.DoesNotExist:
				pass
	
			#If the incident occured on User, notify him.
			#TODO - Update it to notification/alert to the user. 
			if self.target_content_type.model_class()==SchuleUser:
				target_user = SchuleUser.objects.get(pk=self.target_object_id)
				Update.objects.create(incident=self,recepient=target_user,
						timstamp = self.created_at, onself=True)
	
			
		if self.action_object:
			try:
				action_object_follow = Follow.objects.get(object_id=self.action_object_id, content_type=self.action_object_content_type)

				# Add 'self' update for action object if it has more than one followers.
				if action_object_follow.more_than_one_follow():
					action_object_object = self.action_object_content_type.get_object_for_this_type(id=self.action_object_id)
					Update.objects.create(incident=self,recepient=action_object_object, timestamp=self.created_at, onself=True)

				#Update followers of action object.
				action_object_follow.update_followers(self)
			except Follow.DoesNotExist:
				pass
	
			#If action object is user, update.
			#TODO - change this update to notification/Alert.
			if self.action_object_content_type.model_class()==SchuleUser:
				action_object_user = SchuleUser.objects.get(pk=self.action_object_id)
				Update.objects.create(incident=self,recepient=action_object_user, timestamp=self.created_at, onself=True)
		
			
		#Mark the incident as processed.
		self.mark_as_processed()
	
	



class Update(models.Model):
	incident = models.ForeignKey(Incident)
	
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType)
	recepient = generic.GenericForeignKey('content_type', 'object_id')

	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(default=now)
	public = models.BooleanField(default=False)
	onself = models.BooleanField(default=False)

	objects = UpdateManager()

	class Meta:
		ordering = ('-timestamp',)

	def mark_as_read(self):
		self.read =True
		self.save()

	def timesince(self, time_now=None):
		from django.utils.timesince import timesince as _
		return _(self.timestsamp,time_now)

	def __unicode__(self):
		return self.incident.__unicode__()

	def to_html(self):
		return self.incident.to_html()

class Follow(models.Model):
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	leader = generic.GenericForeignKey('content_type','object_id')
	followers = models.ManyToManyField(SchuleUser)

	class Meta:
		unique_together = ('content_type', 'object_id')

	def update_followers(self, incident):
		'''Updates the Update table for followers of any object'''
		try:				
			if incident.actor_content_type.model_class()==SchuleUser:
				followers = self.followers.all().exclude(pk=incident.actor_object_id)
			else:
				followers = target_follow_object.followers.all()
	
			for follower in followers:
				Update.objects.create(incident=incident, recepient=follower, read=False, timestamp=incident.created_at, public=False) 
		except Follow.DoesNotExist:
			pass
	
	def has_follower(self):
		'''Determines whether given object has followers.'''
		if self.followers.count():
			return True
		return False 
	
	def more_than_one_follow(self):
		if self.followers.count() >1 :
			return True
		return False
