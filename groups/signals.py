from django.dispatch import Signal, receiver
from updates.models import Follow


#Signal for saving the corresponding entry in the GroupMembership
#when a new group is added.
CreateGroupMembership = Signal(providing_args=['instance','user','created'])

@receiver(CreateGroupMembership)
def CreateGroupMemHandler(sender,**kwargs):
        from groups.models import GroupMembership

        created =kwargs.get('created')
        if created:
		user = kwargs.get('user')
		group = kwargs.get('group')

                GroupMembership.objects.create(user=user, group=instance, userType='OW')

		#Add follower to the group
		folo=Follow.objects.te(leader=group)
		folo.followers.add(ser)
