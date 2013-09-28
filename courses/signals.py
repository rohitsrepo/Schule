from django.dispatch import Signal, receiver 


#Signal for saving the corresponding entry in the CourseMembership
#when a new course is added.
CreateCourseMembership = Signal(providing_args=['instance','user','created'])

@receiver(CreateCourseMembership)
def CreateCourseMemHandler(sender,**kwargs):
	from courses.models import CourseMembership

	created =kwargs.get('created')
	if created:
		CourseMembership.objects.create(user = kwargs.get('user'),course = kwargs.get('instance'),userType = 'OW')
