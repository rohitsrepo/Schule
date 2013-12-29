from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from forums.forms import GroupForumForm, GroupForumCommentForm
from forums.models import GroupForum, GroupForumComment
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from groups.models import Group


@login_required
def CreateForum(request,group_id):
        group = get_object_or_404(Group,pk = group_id)
        #TODO - implement dynamic add more on the frontend using ajax. Also restrict the number of options that can be added.

        if request.method == 'POST':
                forum_form = GroupForumForm(request.POST, request.FILES)

                if forum_form.is_valid():
                        forum = forum_form.save(commit=False)
                        forum.group = group
                        forum.creater = request.user
                        forum.save()


                        return redirect(reverse('group_forumHome', args=(group.id, forum.id,)))
        else:
                forum_form = GroupForumForm()

        return render_to_response('forums/groups/createForum.html',{
                'group':group,
                'forum_form':forum_form,
                },context_instance=RequestContext(request))


@login_required
def EditForum(request,group_id,forum_id):
        group = get_object_or_404(Group,pk=group_id)
        forum= get_object_or_404(GroupForum,pk=forum_id)
 
        if request.method  == 'POST':
                forum_form = GroupForumForm(request.POST, request.FILES, instance=forum)
               
                if forum_form.is_valid():
                        forum_form.save()
                       
                return redirect(reverse('group_forum_edit', args=(group_id, forum_id)))

        else:
                forum_form = GroupForumForm(instance=forum)
                
        return render_to_response('forums/groups/editForum.html',{
                'group':group,
                'forum_form':forum_form,
                'forum':forum,
                },context_instance=RequestContext(request))

#Permissions
@login_required
def ForumsHome(request,group_id):
        #pull out all the forums for this group
        group = get_object_or_404(Group,pk=group_id)
        try:
                forums = GroupForum.objects.filter(group=group_id).order_by('-id')
        except GroupForum.DoesNotExist:
                raise Http404

        paginator = Paginator(forums,7)
        page = request.GET.get('page')

        try:
                forum_list = paginator.page(page)
        except PageNotAnInteger:
                forum_list = paginator.page(1)
        except EmptyPage:
                forum_list = paginator.page(paginator.num_pages)

        #show by pagination
        return render_to_response('forums/groups/forumsHome.html',{
                'group':group,
                'forums':forum_list,
                })

@login_required
def ForumHome(request,group_id,forum_id):
        #implement voting - change number of votes- take care of revote - redirect to results in case already voted
        group = get_object_or_404(Group,pk=group_id)
        try:
                forum = GroupForum.objects.get(pk=forum_id)
                
                if request.method == 'POST':
                	comment_form = GroupForumCommentForm(request.POST) 
			
			if comment_form.is_valid():
				comment_object = comment_form.save(commit=False)
				comment_object.commenter = request.user
				comment_object.forum = forum
				comment_object.save()

                        	return redirect(reverse('group_forumHome', args=(group_id,forum_id,)))
		else:
			comment_form = GroupForumCommentForm()

		comments = GroupForumComment.objects.filter(forum=forum)


        except GroupForum.DoesNotExist:
                raise Http404
	except GroupForumComment.DoesNotExist:
		comments = []

        return render_to_response('forums/groups/forumHome.html',{
                'group':group,
                'forum':forum,
                'comments':comments,
		'comment_form':comment_form,
                },context_instance=RequestContext(request))

