from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from forums.forms import CourseForumForm, CourseForumCommentForm
from forums.models import CourseForum, CourseForumComment
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from courses.models import Course


@login_required
def CreateForum(request,course_id):
        course = get_object_or_404(Course,pk = course_id)
        #TODO - implement dynamic add more on the frontend using ajax. Also restrict the number of options that can be added.

        if request.method == 'POST':
                forum_form = CourseForumForm(request.POST, request.FILES)

                if forum_form.is_valid():
                        forum = forum_form.save(commit=False)
                        forum.course = course
                        forum.creater = request.user
                        forum.save()


                        return redirect(reverse('course_forumHome', args=(course.id, forum.id,)))
        else:
                forum_form = CourseForumForm()

        return render_to_response('forums/courses/createForum.html',{
                'course':course,
                'forum_form':forum_form,
                },context_instance=RequestContext(request))


@login_required
def EditForum(request,course_id,forum_id):
        course = get_object_or_404(Course,pk=course_id)
        forum= get_object_or_404(CourseForum,pk=forum_id)
 
        if request.method  == 'POST':
                forum_form = CourseForumForm(request.POST, request.FILES, instance=forum)
               
                if forum_form.is_valid():
                        forum_form.save()
                       
                return redirect(reverse('course_forum_edit', args=(course_id, forum_id)))

        else:
                forum_form = CourseForumForm(instance=forum)
                
        return render_to_response('forums/courses/editForum.html',{
                'course':course,
                'forum_form':forum_form,
                'forum':forum,
                },context_instance=RequestContext(request))

#Permissions
@login_required
def ForumsHome(request,course_id):
        #pull out all the forums for this course
        course = get_object_or_404(Course,pk=course_id)
        try:
                forums = CourseForum.objects.filter(course=course_id).order_by('-id')
        except CourseForum.DoesNotExist:
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
        return render_to_response('forums/courses/forumsHome.html',{
                'course':course,
                'forums':forum_list,
                })

@login_required
def ForumHome(request,course_id,forum_id):
        #implement voting - change number of votes- take care of revote - redirect to results in case already voted
        course = get_object_or_404(Course,pk=course_id)
        try:
                forum = CourseForum.objects.get(pk=forum_id)
                
                if request.method == 'POST':
                	comment_form = CourseForumCommentForm(request.POST) 
			
			if comment_form.is_valid():
				comment_object = comment_form.save(commit=False)
				comment_object.commenter = request.user
				comment_object.forum = forum
				comment_object.save()

                        	return redirect(reverse('course_forumHome', args=(course_id,forum_id,)))
		else:
			comment_form = CourseForumCommentForm()

		comments = CourseForumComment.objects.filter(forum=forum)


        except CourseForum.DoesNotExist:
                raise Http404
	except CourseForumComment.DoesNotExist:
		comments = []

        return render_to_response('forums/courses/forumHome.html',{
                'course':course,
                'forum':forum,
                'comments':comments,
		'comment_form':comment_form,
                },context_instance=RequestContext(request))

