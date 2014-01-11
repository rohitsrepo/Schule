from django.dispatch import Signal, receiver 
from updates.models import Follow

#Signal for saving the corresponding entry in the CourseMembership
#when a new course is added.
CreateCourseMembership = Signal(providing_args=['instance','user','created'])

@receiver(CreateCourseMembership)
def CreateCourseMemHandler(sender,**kwargs):
	from courses.models import CourseMembership

	created =kwargs.get('created')
	if created:
		user = kwargs.get('user')
		course = kwargs.get('instance')

		CourseMembership.objects.create(user = user,course = course,userType = 'OW')
		
		#Add follower to the course.
		folo = Follow.objects.create(leader=course)
		folo.followers.add(user)
