from django.forms import ModelForm,ModelChoiceField
from django import forms
from courses.models import Course,CourseMembership
from accounts.models import SchuleUser
from datetime import date

class CourseForm(ModelForm):
	startDate = forms.DateField(initial= date.today())
	class Meta:
		model = Course
		fields = ['name','description','startDate','endDate','coursePhoto','courseVideo']

class UserModelChoiceField(ModelChoiceField):
	def label_from_instance(self,obj):
		#return obj.get_full_name()
		return obj.username

class CourseMemberForm(ModelForm):
	# May be just user should be added
	user = UserModelChoiceField(queryset=SchuleUser.objects.all())
	class Meta:
		model = CourseMembership
		fields = ['user','userType']
	def __init__(self,*args,**kwargs):
		courseId = kwargs.pop('course_id',None)
		super(CourseMemberForm,self).__init__(*args,**kwargs)
		if courseId is not None:
			try:
				self.fields['user'].queryset = SchuleUser.objects.exclude(coursemembership__course__id__exact=courseId)
			except SchuleUser.DoesNotExist:
				#Update this, might return erro in userModelChoice field in order to access username
				self.fields['user'].queryset = None

