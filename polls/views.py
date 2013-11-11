from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from polls.forms import CoursePollForm
from courses.models import Course
from polls.models import CoursePoll, CoursePollOption
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import modelformset_factory
from django.http import Http404


#TODO - Ajaxify the call on the frontend
#	to reduce number of queries in following views
#	for example we should not be reuired to query for course
#	every time we see any of these pages. 
#	These views should just concern themselves with poll data


#Permissions
@login_required
def CreatePoll(request,course_id):
	course = get_object_or_404(Course,pk = course_id)
	#TODO - implement dynamic add more on the frontend using ajax.
	poll_op_model_formset = modelformset_factory(CoursePollOption, fields=('name',), extra=2, max_num=4)

	if request.method == 'POST':
		poll_form = CoursePollForm(request.POST)
		poll_op_formset = poll_op_model_formset(request.POST)

		if poll_form.is_valid() and poll_op_formset.is_valid():
			poll = poll_form.save(commit=False)
			poll.course = course
			poll.creater = request.user
			poll.save()
			
			poll_ops = poll_op_formset.save(commit = False)
			for poll_op in poll_ops:
				poll_op.poll = poll
				poll_op.save()
				
			return redirect(reverse('pollHome', args=(course.id, poll.id,)))
	else:
		poll_form = CoursePollForm()
		poll_op_formset = poll_op_model_formset()

	return render_to_response('courses/createPoll.html',{
		'course':course,
		'poll_form':poll_form,
		'poll_op_formset':poll_op_formset,
		},context_instance=RequestContext(request))

#Permissions
@login_required
def PollsHome(request,course_id):
	#pull out all the polls for this course
	course = get_object_or_404(Course,pk=course_id)
	try:
		polls = CoursePoll.objects.filter(course=course_id)
	except CoursePoll.DoesNotExist:
		raise Http404
		
	paginator = Paginator(polls,10)
	page = request.GET.get('page')
	
	try:
		poll_list = paginator.page(page)
	except PageNotAnInteger:
		poll_list = paginator.page(1)
	except EmptyPage:
		poll_list = paginator.page(paginator.num_pages)
	
	#show by pagination
	return render_to_response('courses/pollsHome.html',{
		'course':course,
		'polls':poll_list,
		})

#Permissios
@login_required
def PollHome(request,course_id,poll_id):
	#implement voting - change number of votes- take care of revote - redirect to results in case already voted
	course = get_object_or_404(Course,pk=course_id)
	try:
		poll = CoursePoll.objects.get(pk=poll_id)
		poll_ops = CoursePollOption.objects.filter(poll = poll)

		# If user has already voted -> redirect
		#voter_ids = [voter.id for voter in poll.voters]
		if len(poll.voters.filter(pk=request.user.id)) >0:
			return redirect(reverse('pollStatus', args=(course_id,poll_id,)))
		
		if request.method == 'POST':
			selected_poll_op_id = request.POST.get('vote')
			selected_poll_op = CoursePollOption.objects.get(pk=selected_poll_op_id)
			selected_poll_op.votes += 1
			selected_poll_op.save()
	
			poll.voters.add(request.user.id)
			
			return redirect(reverse('pollStatus', args=(course_id,poll_id,)))

	except (CoursePoll.DoesNotExist, CoursePollOption.DoesNotExist) as e:
		raise Http404
	
	return render_to_response('courses/pollHome.html',{
		'course':course,
		'poll':poll,
		'poll_ops':poll_ops,
		},context_instance=RequestContext(request))

#Permissions
@login_required
def PollStatus(request,course_id,poll_id):
	course = get_object_or_404(Course,pk = course_id)
	poll = get_object_or_404(CoursePoll,pk = poll_id)
	try:
		poll_ops = CoursePollOption.objects.filter(poll = poll_id)
	except CoursePollOptions.DoesNotExist:
		#TODO - return page saying no options have been created yet for this poll
		raise Http404

	return render_to_response('courses/pollResult.html',{
		'course':course,
		'poll':poll,
		'poll_ops':poll_ops,
		})
