from django.forms import ModelForm
from polls.models import CoursePoll

class CoursePollForm(ModelForm):
	class Meta:
		model = CoursePoll
		fields = ['title', 'description']


