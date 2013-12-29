from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from polls.forms import GroupPollForm, GroupPollOptionForm
from groups.models import Group
from polls.models import GroupPoll, GroupPollOption
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import inlineformset_factory
from django.http import Http404


#TODO - Ajaxify the call on the frontend
#	to reduce number of queries in following views
#	for example we should not be reuired to query for group
#	every time we see any of these pages. 
#	These views should just concern themselves with poll data


#Permissions
@login_required
def CreatePoll(request,group_id):
	group = get_object_or_404(Group,pk = group_id)
	#TODO - implement dynamic add more on the frontend using ajax. Also restrict the number of options that can be added.
	
	if request.method == 'POST':
		poll_form = GroupPollForm(request.POST, request.FILES)
		
		if poll_form.is_valid():
			poll = poll_form.save(commit=False)
			poll.group = group
			poll.creater = request.user
			poll.save()
			
						
			return redirect(reverse('group_poll_op', args=(group.id, poll.id,)))
	else:
		poll_form = GroupPollForm()
		
	return render_to_response('polls/groups/createPoll.html',{
		'group':group,
		'poll_form':poll_form,
		},context_instance=RequestContext(request))

@login_required
def CreatePollOption_old(request,group_id,poll_id):
	group = get_object_or_404(Group,pk = group_id)
	poll = get_object_or_404(GroupPoll,pk =poll_id)

	poll_op_inline_formset = inlineformset_factory(GroupPoll,GroupPollOption,extra=2)
	
	if request.method == 'POST':
                poll_op_formset = poll_op_inline_formset(request.POST,instance=poll)

                if poll_op_formset.is_valid():
			poll_op_formset.save()
                        return redirect(reverse('group_pollHome', args=(group.id, poll.id,)))
        else:
                poll_op_formset = poll_op_inline_formset(instance=poll)

	return render_to_response('polls/groups/addPollOp.html',{
		'group':group,
		'poll':poll,
		'poll_op_fomset':poll_op_formset,
		},context_instance=RequestContext(request))
		
@login_required
def CreatePollOption(request,group_id,poll_id):
	group = get_object_or_404(Group,pk=group_id)
	poll = get_object_or_404(GroupPoll,pk = poll_id)

	try:
		poll_ops = GroupPollOption.objects.filter(poll=poll_id)
	except GroupPollOption.DoesNotExist:
		poll_ops = []

	if request.method == 'POST':
		form = GroupPollOptionForm(request.POST)
		op = form.save(commit=False)

		op.poll = poll
		op.save()
	
		return redirect(reverse('group_poll_op', args=(group_id,poll_id)))

	else:
		form = GroupPollOptionForm()

	return render_to_response('polls/groups/addPollOp.html',{
		'group':group,
		'poll':poll,
		'form':form,
		'poll_ops':poll_ops
		},context_instance=RequestContext(request))

@login_required
def EditPoll(request,group_id,poll_id):
	group = get_object_or_404(Group,pk=group_id)
	poll= get_object_or_404(GroupPoll,pk=poll_id)

	poll_op_inlineformset = inlineformset_factory(GroupPoll,GroupPollOption,extra=1, fields=('name',))

	if request.method  == 'POST':
		poll_form = GroupPollForm(request.POST,instance=poll)
		poll_op_formset = poll_op_inlineformset(request.POST, instance=poll)

		if poll_form.is_valid() and poll_op_formset.is_valid():
			poll_form.save()
			poll_op_formset.save()

		return redirect(reverse('group_poll_edit', args=(group_id, poll_id)))

	else:
		poll_form = GroupPollForm(instance=poll)
		poll_op_formset  = poll_op_inlineformset(instance=poll)		

	return render_to_response('polls/groups/editPoll.html',{
		'group':group,
		'poll_form':poll_form,
		'poll_op_formset':poll_op_formset,
		'poll':poll,
		},context_instance=RequestContext(request))

#Permissions
@login_required
def PollsHome(request,group_id):
	#pull out all the polls for this group
	group = get_object_or_404(Group,pk=group_id)
	try:
		polls = GroupPoll.objects.filter(group=group_id).order_by('-id')
	except GroupPoll.DoesNotExist:
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
	return render_to_response('polls/groups/pollsHome.html',{
		'group':group,
		'polls':poll_list,
		})

#Permissios
@login_required
def PollHome(request,group_id,poll_id):
	#implement voting - change number of votes- take care of revote - redirect to results in case already voted
	group = get_object_or_404(Group,pk=group_id)
	try:
		poll = GroupPoll.objects.get(pk=poll_id)

		# If user has already voted -> redirect
		#voter_ids = [voter.id for voter in poll.voters]
		if len(poll.voters.filter(pk=request.user.id)) >0:
			return redirect(reverse('group_pollStatus', args=(group_id,poll_id,)))
		
		if request.method == 'POST':
			selected_poll_op_id = request.POST.get('vote')
			selected_poll_op = GroupPollOption.objects.get(pk=selected_poll_op_id)
			selected_poll_op.votes += 1
			selected_poll_op.save()
	
			poll.voters.add(request.user.id)
			
			return redirect(reverse('group_pollStatus', args=(group_id,poll_id,)))

		poll_ops = GroupPollOption.objects.filter(poll = poll)


	except GroupPoll.DoesNotExist:
		raise Http404
	except GroupPollOption.DoesNotExist:
		poll_ops=[]
	
	return render_to_response('polls/groups/pollHome.html',{
		'group':group,
		'poll':poll,
		'poll_ops':poll_ops,
		},context_instance=RequestContext(request))

#Permissions
@login_required
def PollStatus(request,group_id,poll_id):
	group = get_object_or_404(Group,pk = group_id)
	poll = get_object_or_404(GroupPoll,pk = poll_id)
	try:
		poll_ops = GroupPollOption.objects.filter(poll = poll_id)
	except GroupPollOptions.DoesNotExist:
		#TODO - return page saying no options have been created yet for this poll
		raise Http404

	return render_to_response('polls/groups/pollResult.html',{
		'group':group,
		'poll':poll,
		'poll_ops':poll_ops,
		})
