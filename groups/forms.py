from django.forms import ModelForm,ModelChoiceField
from django import forms
from groups.models import Group, GroupMembership, GroupResource
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

class GroupForm(ModelForm):
        startDate = forms.DateField(initial= date.today())
        groupPhoto = ExtFileField(ext_whitelist = settings.AUDIO_FILE, required=False, allow_empty_file =False, max_length =20)
        groupVideo = ExtFileField(ext_whitelist = settings.VIDEO_FILE, required=False, allow_empty_file =False, max_length =20)
        class Meta:
                model = Group
                fields = ['name','description','startDate','groupPhoto','groupVideo']

class UserModelChoiceField(ModelChoiceField):
        def label_from_instance(self,obj):
                #return obj.get_full_name()
                return obj.username

class GroupMemberForm(ModelForm):
        # May be just user should be added
        user = UserModelChoiceField(queryset=SchuleUser.objects.all())
        class Meta:
                model = GroupMembership
                fields = ['user','userType']
        def __init__(self,*args,**kwargs):
                groupId = kwargs.pop('group_id',None)
                super(GroupMemberForm,self).__init__(*args,**kwargs)
                if groupId is not None:
                        try:
                                self.fields['user'].queryset = SchuleUser.objects.exclude(groupmembership__group__id__exact=groupId)
                        except SchuleUser.DoesNotExist:
                                #Update this, might return erro in userModelChoice field in order to access username
                                self.fields['user'].queryset = None


class GroupResourceForm(ModelForm):
        data = ExtFileField(ext_whitelist = settings.COURSE_RESOURCE_FILE, required=True, allow_empty_file =False, max_length =20)

        class Meta:
                model = GroupResource
                fields =['title','description','data']

