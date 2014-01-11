from .models import Incident, Update, Follow
from accounts.models import SchuleUser
from django.contrib.contenttypes.models import ContentType


def clear_incident_backlog():
	'''Reads all unprocessed incidents and creates corresponsing incidents.'''
	
	try:
		incidents = Incident.objects.filter(processed=False)
		for incident in incidents:
			create_update(incident)
	except Incident.DoesNotExist:
		pass



def create_update(incident):
	'''Takes incident object/id as arguments
	   And creates updates for user based on 
	   Follow table. '''	

	if isinstance(incident, Incident):
		if not incident.pk:
			raise Exception("create_update: incident passed is not present in db")
	elif isinstance(incident, int):
		incident = Incident.objects.get(pk=incident).select_related('actor', 'target', 'action_object')

	actor = incident.actor
	target = incident.target
	action_object = incident.action_object

	if target:
		#add update for target object ifit has followers.
		if has_follower(incident.target_object_id, incident.target_content_type):
			target_object = incident.target_content_type.get_object_for_this_type(id=incident.target_object_id)
			Update.objects.create(incident= incident, recepient=target_object, timestamp = incident.created_at, onself=True)
			#Update the followers of this object.
			update_followers(incident.target_object_id, incident.target_content_type, incident)



		#If the incident occured on User, notify him.
		#TODO - Update it to notification/alert to the user. 
		if incident.target_content_type.model_class()==SchuleUser:
			target_user = SchuleUser.objects.get(pk=incident.target_object_id)
			Update.objects.create(incident=incident,recepient=target_user,
					timstamp = incident.created_at, onself=True)

		
	if action_object:
		# Add update for action object if it has followers.
		if has_follower(incident.action_object_id, incident.action_object_content_type):
			action_object_object = incident.action_object_content_type.get_object_for_this_type(id=incident.action_object_id)
			Update.objects.create(incident=incident,recepient=action_object_object, timestamp=incident.created_at, onself=True)
			#Update followers of action object.
			update_followers(incident.action_object_id, incident.action_object_content_type,incident)
	

		#If action object is user, update.
		#TODO - change this update to notification/Alert.
		if incident.action_object_content_type.model_class()==SchuleUser:
			action_object_user = SchuleUser.objects.get(pk=incident.action_object_id)
			Update.objects.create(incident=incident,recepient=action_object_user, timestamp=incident.created_at, onself=True)
	
		
	#Mark the incident as processed.
	incident.mark_as_processed()
	
	

def update_followers(object_id,content_type_id, incident):
	'''Updates the Update table for followers of any object'''
	try:
		target_follow_object = Follow.objects.get(content_type=content_type_id, object_id=object_id)

		if incident.actor_content_type.model_class()==SchuleUser:
			followers = target_follow_object.followers.all().exclude(pk=incident.actor_object_id)
		else:
			followers = target_follow_object.followers.all()

		for follower in followers:
			Update.objects.create(incident=incident, recepient=follower, read=False, timestamp=incident.created_at, public=False) 
	except Follow.DoesNotExist:
		pass

def has_follower(object_id, content_type):
	'''Determines whether given object has followers.'''
	try:
		follow = Follow.objects.get(content_type = content_type, object_id=object_id)
		if follow.followers.count():
			return True
	except Follow.DoesNotExist:
		pass

	return False 

#Move it to model manager of updates.
def get_updates(recepient, target=None):
	'''Gets updates for 'recepient'.
	   Filtered with target object in case one is provided.'''

	try:
		recep_content = ContentType.objects.get_for_model(recepient)

		if target:
			target_content = ContentType.objects.get_for_model(target)
			updates = Update.objects.filter(content_type=recep_content, object_id=recepient.id, incident__target_object_id__exact=target.id,incident__target_content_type__exact=target_content)
		else:
			updates = Update.objects.filter(content_type=recep_content, object_id=recepient.id)

	except Update.DoesNotExist:
		updates =[]

	return updates
