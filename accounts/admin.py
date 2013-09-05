#Added for future use
#Currently using django 'UserAdmin' for the SchuleUser

from accounts.forms import UserRegistrationForm, UserChangeForm
from accounts.models import SchuleUser
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from accounts.Utility import GenVigKey

class SchuleUserAdmin(ModelAdmin):
    '''Admin class for SchuleUser'''    
    
    #exclude = ('vigilanceKey',)

    form = UserChangeForm
    add_form = UserRegistrationForm   

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(SchuleUserAdmin, self).get_form(request, obj, **defaults)   

    def save_model(self,request,obj,form,change):
	# Generate vigilance key for user
	obj.vigilanceKey = GenVigKey()
	obj.save()
    

admin.site.register(SchuleUser,SchuleUserAdmin)

"""class SchuleUserAdmin_notUsed(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password','userType')}),
        ('Personal info', {'fields': ('birthDate',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
"""
