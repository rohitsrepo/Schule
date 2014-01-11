from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from polls.forms import CoursePollForm, CoursePollOptionForm
from courses.models import Course
from updates.models import Incident, Follow
from polls.models import CoursePoll, CoursePollOption
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import inlineformset_factory
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
	#TODO - implement dynamic add more on the frontend using ajax. Also restrict the number of options that can be added.
	
	if request.method == 'POST':
		poll_form = CoursePollForm(request.POST, request.FILES)
		
		if poll_form.is_valid():
			poll = poll_form.save(commit=False)
			poll.course = course
			poll.creater = request.user
			poll.save()
			
			#Create corresponding incident.
			Incident.objects.create(actor=request.user, verb='added', target=course, action_object=poll)	

			return redirect(reverse('course_poll_op', args=(course.id, poll.id,)))
	else:
		poll_form = CoursePollForm()
		
	return render_to_response('polls/courses/createPoll.html',{
		'course':course,
		'poll_form':poll_form,
		},context_instance=RequestContext(request))

@login_required
def CreatePollOption_old(request,course_id,poll_id):
	course = get_object_or_404(Course,pk = course_id)
	poll = get_object_or_404(CoursePoll,pk =poll_id)

	poll_op_inline_formset = inlineformset_factory(CoursePoll,CoursePollOption,extra=2)
	
	if request.method == 'POST':
                poll_op_formset = poll_op_inline_formset(request.POST,instance=poll)

                if poll_op_formset.is_valid():
			poll_op_formset.save()
                        return redirect(reverse('course_pollHome', args=(course.id, poll.id,)))
        else:
                poll_op_formset = poll_op_inline_formset(instance=poll)

	return render_to_response('polls/courses/addPollOp.html',{
		'course':course,
		'poll':poll,
		'poll_op_fomset':poll_op_formset,
		},context_instance=RequestContext(request))
		
@login_required
def CreatePollOption(request,course_id,poll_id):
	course = get_object_or_404(Course,pk=course_id)
	poll = get_object_or_404(CoursePoll,pk = poll_id)

	try:
		poll_ops = CoursePollOption.objects.filter(poll=poll_id)
	except CoursePollOption.DoesNotExist:
		poll_ops = []

	if request.method == 'POST':
		form = CoursePollOptionForm(request.POST)
		op = form.save(commit=False)

		op.poll = poll
		op.save()
	
		return redirect(reverse('course_poll_op', args=(course_id,poll_id)))

	else:
		form = CoursePollOptionForm()

	return render_to_response('polls/courses/addPollOp.html',{
		'course':course,
		'poll':poll,
		'form':form,
		'poll_ops':poll_ops
		},context_instance=RequestContext(request))

@login_required
def EditPoll(request,course_id,poll_id):
	course = get_object_or_404(Course,pk=course_id)
	poll= get_object_or_404(CoursePoll,pk=poll_id)

	poll_op_inlineformset = inlineformset_factory(CoursePoll,CoursePollOption,extra=1, fields=('name',))

	if request.method  == 'POST':
		poll_form = CoursePollForm(request.POST,instance=poll)
		poll_op_formset = poll_op_inlineformset(request.POST, instance=poll)

		if poll_form.is_valid() and poll_op_formset.is_valid():
			poll_form.save()
			poll_op_formset.save()

			#Create an incident.
			Incident.objects.create(actor=request.user, target=course, action_object=poll, verb='editted')


		return redirect(reverse('course_poll_edit', args=(course_id, poll_id)))

	else:
		poll_form = CoursePollForm(instance=poll)
		poll_op_formset  = poll_op_inlineformset(instance=poll)		

	return render_to_response('polls/courses/editPoll.html',{
		'course':course,
		'poll_form':poll_form,
		'poll_op_formset':poll_op_formset,
		'poll':poll,
		},context_instance=RequestContext(request))

#Permissions
@login_required
def PollsHome(request,course_id):
	#pull out all the polls for this course
	course = get_object_or_404(Course,pk=course_id)
	try:
		polls = CoursePoll.objects.filter(course=course_id).order_by('-id')
	except CoursePoll.DoesNotExist:
		raise Http404
		
	paginator = Paginator(polls,7)
	page = request.GET.get('page')
	
	try:
		poll_list = paginator.page(page)
	except PageNotAnInteger:
		poll_list = paginator.page(1)
	except EmptyPage:
		poll_list = paginator.page(paginator.num_pages)
	
	#show by pagination
	return render_to_response('polls/courses/pollsHome.html',{
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

		# If user has already voted -> redirect
		#voter_ids = [voter.id for voter in poll.voters]
		if len(poll.voters.filter(pk=request.user.id)) >0:
			return redirect(reverse('course_pollStatus', args=(course_id,poll_id,)))
		
		if request.method == 'POST':
			selected_poll_op_id = request.POST.get('vote')
			selected_poll_op = CoursePollOption.objects.get(pk=selected_poll_op_id)
			selected_poll_op.votes += 1
			selected_poll_op.save()
	
			poll.voters.add(request.user.id)
			
			return redirect(reverse('course_pollStatus', args=(course_id,poll_id,)))

		poll_ops = CoursePollOption.objects.filter(poll = poll)


	except CoursePoll.DoesNotExist:
		raise Http404
	except CoursePollOption.DoesNotExist:
		poll_ops=[]
	
	return render_to_response('polls/courses/pollHome.html',{
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

	return render_to_response('polls/courses/pollResult.html',{
		'course':course,
		'poll':poll,
		'poll_ops':poll_ops,
		})
