from django.db import models
from django.contrib.contenttypes.models import ContentType

class UpdateManager(models.Manager):	
	def get_updates(self, recepient, target=None):
		'''Gets updates for 'recepient'.
		   Filtered with target object in case one is provided.'''
	
		try:
			recep_content = ContentType.objects.get_for_model(recepient)
	
			if target:
				target_content = ContentType.objects.get_for_model(target)
				updates = self.get_queryset().filter(content_type=recep_content, object_id=recepient.id, incident__target_object_id__exact=target.id,incident__target_content_type__exact=target_content)
			else:
				updates = self.get_queryset().filter(content_type=recep_content, object_id=recepient.id)
	
		except self.model.DoesNotExist:
			updates =[]
		
		return updates

class IncidentManager(models.Manager):
	def clear_backlog(self):
		'''Reads all unprocessed incidents and creates corresponsing incidents.'''
	
		try:
			incidents = self.get_queryset().filter(processed=False)
			for incident in incidents:
				incident.create_update()
		except self.model.DoesNotExist:
			pass
