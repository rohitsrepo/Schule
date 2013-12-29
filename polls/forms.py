from django.forms import ModelForm
from polls.models import CoursePoll, CoursePollOption, GroupPoll, GroupPollOption

class CoursePollForm(ModelForm):
	class Meta:
		model = CoursePoll
		fields = ['title', 'description', 'data']

class CoursePollOptionForm(ModelForm):
	class Meta:
		model = CoursePollOption
		fields = ['name',]

class GroupPollForm(ModelForm):
	class Meta:
		model = GroupPoll
		fields = ['title', 'description', 'data']

class GroupPollOptionForm(ModelForm):
	class Meta:
		model = GroupPollOption
		fields = ['name',]

