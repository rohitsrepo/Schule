from django.forms import ModelForm
from forums.models import CourseForum, CourseForumComment, GroupForum, GroupForumComment

class CourseForumForm(ModelForm):
        class Meta:
                model = CourseForum
                fields = ['title', 'description', 'data']

class CourseForumCommentForm(ModelForm):
        class Meta:
                model = CourseForumComment
                fields = ['comment',]

class GroupForumForm(ModelForm):
        class Meta:
                model = GroupForum
                fields = ['title', 'description', 'data']

class GroupForumCommentForm(ModelForm):
        class Meta:
                model = GroupForumComment
                fields = ['comment',]
