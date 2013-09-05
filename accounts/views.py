from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from accounts.forms import UserRegistrationForm

#User registration
def register(request):
  if request.method =='POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      #user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password1'])
      #user.save()
      form.save()
      return redirect(settings.USER_HOME) # Redirect after POST
  else:
    form = UserRegistrationForm() # An unbound form

  return render_to_response('accounts/register.html', {
    'form': form,
},context_instance=RequestContext(request))

# Generates vigilance key for user
def GenVigKey():
  chars = string.letters + string.digits
  for i in range(8):
    newpasswd = newpasswd + choice(chars)
  return newpasswd

