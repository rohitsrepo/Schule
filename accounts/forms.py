# Customizing the forms required for user accounts.
# Mostly using inbuilt forms from 'django.contrib.auth'


from accounts.models import SchuleUser
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from accounts.Utility import GenVigKey

# Customozed form for registering new users.
class UserRegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {

        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
 
    first_name = forms.CharField(label=_('First Name'), max_length=30, required=True)
    last_name = forms.CharField(label=_('Last Name'), max_length=30, required=True)

    session_user = ''

    def __init__(self,*args,**kwargs):
	if 'user' in kwargs.keys():
	    print "GETTING USER WITH ID" 
	    self.session_user = SchuleUser.objects.get(pk = kwargs.pop('user',None))

	super(UserRegistrationForm,self).__init__(*args,**kwargs)
	
    class Meta:
        model = SchuleUser
       	fields =('username','email','first_name','last_name','userType','addressLine1','addressLine2','state','country','postalCode','countryCode','phone','birthDate')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message.
        username = self.cleaned_data["username"]
        try:
            SchuleUser._default_manager.get(username=username)
        except SchuleUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def clean_userType(self):
	#cleaned_data = super(UserRegistrationForm,self).clean()
	
	userType = self.cleaned_data.get('userType');

	#session_user = request.user
	if(userType == 'IN'):
		if not(self.session_user.has_perm('accounts.create_edit_instructor')):
			raise forms.ValidationError(self.session_user.username+' Does not have permission to create/edit users of type Instructor')
	elif(userType == 'MA'):
		if not(self.session_user.has_perm('accounts.create_edit_manager')):
			raise forms.ValidationError(self.session_user.username+' Does not have permission to create/edit users of type Manager')
	elif(userType=='ST'):
		if not(self.session_user.has_perm('accounts.create_edit_student')):
			raise forms.ValidationError(self.session_user.username+' Does not have permission to create/edit users of type Student')

	return userType

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

	userType = self.cleaned_data.get('userType');

	#session_user = request.user
	if(userType == 'IN'):
		group = Group.objects.get(name='Instructor')
	elif(userType == 'MA'):
		user.is_staff = True
		group = Group.objects.get(name='Manager')
	elif(userType=='ST'):
		group = Group.objects.get(name = 'Student')

	# Generate Vigilance Key for user
	user.vigilanceKey = GenVigKey()
	
        if commit:
            user.save()

	    # Add user to the corresponding Group
	    user.groups.add(group)
	else:
		#TODO: Issue a warning in the logs about group being not added
		pass
        return user

class UserChangeForm(forms.ModelForm):
    '''A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    '''
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SchuleUser
        fields =('username','password','email','first_name','last_name','userType','addressLine1','addressLine2','state','country','postalCode','countryCode','phone','birthDate')

    
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
