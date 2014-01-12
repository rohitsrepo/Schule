from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from accounts.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from accounts.models import SchuleUser
from django.contrib.auth.models import Group
from updates.models import Update
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
  user_updates_list = Update.objects.get_updates(request.user)
  
  paginator = Paginator(user_updates_list, 5)
  page = request.GET.get('page')

  try:
    updates = paginator.page(page)
  except PageNotAnInteger:
    updates = paginator.page(1)
  except EmptyPage:
    updates = paginator.page(paginator.num_pages)

  user_groups = request.user.groups
  if user_groups.filter(name='Student'):
    return render_to_response('accounts/student.html',{
	'updates':updates,
	},context_instance=RequestContext(request))
  elif user_groups.filter(name='Instructor'):
    #TODO-Add a management profile link in instructor profile in case it is manger too
    is_manager = user_groups.filter(name='Manager')
    return render_to_response('accounts/instructor.html',{
	'is_manager':is_manager,
	'updates':updates,
	},context_instance=RequestContext(request))
  elif user_groups.filter(name__in=['Manager','Head Manager']):
    #TODO - If different profile for manager....handle it here
    return redirect('/admin/')
  else:
    #TODO-customize 404 messages
    raise Http404

# Generates vigilance key for user
def GenVigKey():
  chars = string.letters + string.digits
  for i in range(8):
    newpasswd = newpasswd + choice(chars)
  return newpasswd

