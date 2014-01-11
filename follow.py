from updates.models import *
from courses.models import *
from polls.models import *
from accounts.models import *


def create_follower():
	for course in Course.objects.all():
		folo = Follow.objects.create(leader=course)
		for user in course.members.all():
			folo.followers.add(user)


create_follower()
