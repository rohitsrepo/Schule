from django.forms import ModelForm,ModelChoiceField
from django import forms
from courses.models import Course, CourseMembership, CourseResource
from accounts.models import SchuleUser
from datetime import date
from django.conf import settings
import os

class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    """
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
	if data:
        	filename = data.name
        	ext = os.path.splitext(filename)[1]
        	ext = ext.lower()
        	if ext not in self.ext_whitelist:
            		raise forms.ValidationError("Not allowed filetype: %s" % (self.ext_whitelist,))
	return data

class CourseForm(ModelForm):
	startDate = forms.DateField(initial= date.today())
	coursePhoto = ExtFileField(ext_whitelist = settings.AUDIO_FILE, required=False, allow_empty_file =False, max_length =20)
	courseVideo = ExtFileField(ext_whitelist = settings.VIDEO_FILE, required=False, allow_empty_file =False, max_length =20)
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


class CourseResourceForm(ModelForm):
	data = ExtFileField(ext_whitelist = settings.COURSE_RESOURCE_FILE, required=True, allow_empty_file =False, max_length =20)

	class Meta:
		model = CourseResource
		fields =['title','description','data']
