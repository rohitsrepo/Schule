from django.forms import ModelForm
from django import forms
from courses.models import Course
from datetime import date

class CourseForm(ModelForm):
	startDate = forms.DateField(initial= date.today())
	class Meta:
		model = Course
		fields = ['name','description','startDate','endDate','coursePhoto','courseVideo']

