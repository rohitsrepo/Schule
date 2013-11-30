from django.forms import ModelForm
from polls.models import CoursePoll, CoursePollOption

class CoursePollForm(ModelForm):
	class Meta:
		model = CoursePoll
		fields = ['title', 'description']

class CoursePollOptionForm(ModelForm):
	class Meta:
		model = CoursePollOption
		fields = ['name',]
