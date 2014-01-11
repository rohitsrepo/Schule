from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from accounts.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from accounts.models import SchuleUser

#User registration
# Should be only entry point for registering user
def register(request):
  if request.method =='POST':
    form = UserRegistrationForm(request.POST,user=request.user.id)
    if form.is_valid():
      #user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password1'])
      #user.save()
      form.save()
      #TODO- On adding new user, add it to the institute-wide group, ensure update is generated corresponding to user addition.
      return redirect(settings.USER_HOME) # Redirect after POST
  else:
    form = UserRegistrationForm() # An unbound form

  return render_to_response('accounts/register.html', {
    'form': form,
},context_instance=RequestContext(request))


#User home.
@login_required
def userHome(request):
  userType = request.user.userType
  if userType == 'ST':
    return render_to_response('accounts/student.html',
	context_instance=RequestContext(request))
  elif userType =='IN':
    return render_to_response('accounts/instructor.html',
	context_instance=RequestContext(request))
  else:
    return redirect('/admin/')

# Generates vigilance key for user
def GenVigKey():
  chars = string.letters + string.digits
  for i in range(8):
    newpasswd = newpasswd + choice(chars)
  return newpasswd

