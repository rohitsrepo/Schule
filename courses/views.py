from django.shortcuts import render_to_response,redirect
from django.conf import settings
from django.template import RequestContext
from courses.forms import CourseForm
from courses.models import Course,CourseMembership
from courses.signals import CreateCourseMembership 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,get_list_or_404

#Course registration
#permission create and check
@login_required
def RegisterCourse(request):
  if request.method =='POST':
    form = CourseForm(request.POST,request.FILES)
    print "checking for file now"
    if request.FILES:
	print "files present "
    if form.is_valid():
      newCourse = form.save(commit=False)
      newCourse.save()

      CreateCourseMembership.send(sender = Course,instance=newCourse,user=request.user,created = True)
      return redirect(reverse('course_home_url', args(newCourse.id,))) # Redirect after POST
  else:
    form = CourseForm() # An unbound form

  return render_to_response('courses/register.html', {
    'form': form,
},context_instance=RequestContext(request))


#decide on membership policy- members only view....or all with restricted access
@login_required
def CourseHome(request,id):
	course = get_object_or_404(Course,pk = id)
	courseAdmin =get_object_or_404(CourseMembership,course__id__exact =id,userType='OW').user

	courseMods =[]
	try:
		courseWithMods = CourseMembership.objects.filter(course__id__exact = id,userType="MO")
		courseMods = [course.user for course in courseWithMods]
	except CourseMembership.DoesNotExist:
		pass
	return render_to_response('courses/course.html',{
		'course':course,
		'courseAdmin':courseAdmin,
		'courseMods':courseMods,
		})
