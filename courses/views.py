from django.shortcuts import render_to_response,redirect
from django.conf import settings
from django.template import RequestContext
from courses.forms import CourseForm, CourseMemberForm, CourseResourceForm
from courses.models import Course, CourseMembership, CourseResource
#from courses.signals import CreateCourseMembership 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from accounts.models import SchuleUser
from django.http import HttpResponseNotFound
#Course registration
#permission create and check

@login_required
def RegisterCourse(request):
	if request.method =='POST':
    		form = CourseForm(request.POST,request.FILES)

		if form.is_valid():
			newCourse = form.save(commit=False)
			newCourse.save(user = request.user)
	
			#CreateCourseMembership.send(sender = Course,instance=newCourse,user=request.user,created = True)
			return redirect(reverse('course_home', args=(newCourse.id,))) # Redirect after POST
	else:
		form = CourseForm() # An unbound form

	return render_to_response('courses/register.html', {
    		'form': form,
	},context_instance=RequestContext(request))

@login_required
def CoursePage(request):
	return render_to_response('courses/coursePage.html',{
	'events':'',
	},context_instance=RequestContext(request))

#decide on membership policy- members only view....or all with restricted access
@login_required
def CourseHome(request,id):
	print "retieveing course with id : " +id
	course = get_object_or_404(Course,pk = id)
	print "got course with id : "+ str(course.id)
	courseAdmin =get_object_or_404(CourseMembership,course__id__exact =id,userType='OW').user

	courseModMembers =[]
	try:
		courseModMembers = CourseMembership.objects.filter(course__id__exact = id,userType="MO")
		#courseMods = [courseMember.user for courseMember in courseWithMods]
	except CourseMembership.DoesNotExist:
		pass
	print "passing to template : " +str(course.id)
	return render_to_response('courses/course.html',{
		'course':course,
		'courseAdmin':courseAdmin,
		'courseMods':courseModMembers,
		})


#decide on permission and execution policy
@login_required
def CourseMember(request,id):
	course = get_object_or_404(Course,pk=id)	
	courseMembers = (get_list_or_404(CourseMembership.objects.all().order_by('user'),course__id__exact=id))
	
	if request.method == 'POST':
		form = CourseMemberForm(request.POST)
		
		if form.is_valid():
			new_member = form.save(commit=False)
			new_member.course = course
			new_member.save()

			return redirect(reverse('course_member',args=(id,)))
	else:
		form = CourseMemberForm(course_id=id)
	return render_to_response('courses/courseMember.html', {
			'form': form,
			'course':course,
			'courseMembers':courseMembers,
			},context_instance=RequestContext(request))


#Decide Permission
@login_required
def FlipMembership(request,course_id,user_id):
	course = get_object_or_404(CourseMembership,course__id__exact =course_id,user__id=user_id)
	if(course.userType=='MO'):
		course.userType = 'ST'
	elif(course.userType == 'ST'):
		course.userType = 'MO'
	elif(course.userType=='OW'):
		pass
	else:
		return HttpResponseNotFound("<h1>Not a valid request</h1>")

	course.save()
	#respond by redirecting to original page.
	return redirect(reverse('course_member',args=(course_id,)))

	#redirect(request.META.HTTP_REFERER)
	
@login_required
def UserCourses(request,user_id=None):
	if user_id is None:
		user_id = request.user.id
		user = request.user
	else:
		user = get_object_or_404(SchuleUser,pk=user_id)		
	
	try:
		course_list = user.course_set.all().order_by('-startDate')
	except Course.DoesNotExist:
		course_list =[]
	
	paginator = Paginator(course_list,5)
	page = request.GET.get('page')

	try:
		courses = paginator.page(page)
	except PageNotAnInteger:
		courses = paginator.page(1)
	except EmptyPage:
		courses = paginator.page(paginator.num_pages)

	return render_to_response('courses/MyCourse.html',{
		'courses':courses,
	},context_instance=RequestContext(request))

@login_required
def AllCourses(request):
	try:
		course_list = Course.objects.all().order_by('-startDate')
	except Course.DoesNotExist:
		course_list =[]
	
	paginator = Paginator(course_list,5)
	page = request.GET.get('page')

	try:
		courses = paginator.page(page)
	except PageNotAnInteger:
		courses = paginator.page(1)
	except EmptyPage:
		courses = paginator.page(paginator.num_pages)

	return render_to_response('courses/AllCourse.html',{
		'courses':courses,
	},context_instance=RequestContext(request))


@login_required
def RegisterCourseResource(request,course_id):
	course = get_object_or_404(Course,pk=course_id)
	
	if request.method == 'POST':
		form = CourseResourceForm(request.POST,request.FILES)
	
		if form.is_valid():
			res = form.save(commit=False)
			res.course = course
			res.save()
			
			return redirect(reverse('course_resource_page' , args=(course_id, )))
	
	else:
		form = CourseResourceForm()

	return render_to_response('courses/registerResource.html',{
		'course':course,
		'form':form,
	},context_instance=RequestContext(request))

@login_required
def CourseResourcePage(request,course_id):
	course = get_object_or_404(Course,pk = course_id)
	try:
		res_list = CourseResource.objects.filter(course = course_id).order_by('-date')
	except CourseResource.DoesNotExist:
		res_list = []

	paginator = Paginator(res_list,7)

	page = request.GET.get('page')

	try:
		res = paginator.page(page)
	except PageNotAnInteger:
		res = paginator.page(1)
	except EmptyPage:
		res = paginator.page(paginator.num_pages)

	return render_to_response('courses/courseResource.html',{
		'resources':res,
		'course':course,
	},context_instance=RequestContext(request))

	
	
@login_required
def CourseResourceHome(request,course_id,res_id):
	course = get_object_or_404(Course,pk=course_id)

	try:
		res = CourseResource.objects.get(pk=res_id)
	except CourseResource.DoesNotExist:
		res = []

	return render_to_response('courses/courseResourceHome.html',{
		'course':course,
		'resource':res,
		},context_instance=RequestContext(request))
