from django.forms import ModelForm
from forums.models import CourseForum, CourseForumComment

class CourseForumForm(ModelForm):
        class Meta:
                model = CourseForum
                fields = ['title', 'description', 'data']

class CourseForumCommentForm(ModelForm):
        class Meta:
                model = CourseForumComment
                fields = ['comment',]
