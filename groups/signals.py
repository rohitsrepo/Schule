from django.dispatch import Signal, receiver


#Signal for saving the corresponding entry in the GroupMembership
#when a new group is added.
CreateGroupMembership = Signal(providing_args=['instance','user','created'])

@receiver(CreateGroupMembership)
def CreateGroupMemHandler(sender,**kwargs):
        from groups.models import GroupMembership

        created =kwargs.get('created')
        if created:
                GroupMembership.objects.create(user = kwargs.get('user'),group = kwargs.get('instance'),userType = 'OW')

