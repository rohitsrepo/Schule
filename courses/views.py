from django.shortcuts import render_to_response,redirect
from django.conf import settings
from django.template import RequestContext
from courses.forms import CourseForm
from courses.models import Course,CourseMembership
from courses.signals import CreateCourseMembership 
from django.contrib.auth.decorators import login_required


#Course registration
#permission create and check
@login_required
def registerCourse(request):
  if request.method =='POST':
    form = CourseForm(request.POST,request.FILES)
    print "checking for file now"
    if request.FILES:
	print "files present "
    if form.is_valid():
      newCourse = form.save(commit=False)
      newCourse.save()

      CreateCourseMembership.send(sender = Course,instance=newCourse,user=request.user,created = True)
      return redirect(settings.HOME) # Redirect after POST
  else:
    form = CourseForm() # An unbound form

  return render_to_response('courses/register.html', {
    'form': form,
},context_instance=RequestContext(request))
