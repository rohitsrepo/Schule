from django.shortcuts import render_to_response,redirect
from django.conf import settings
from django.template import RequestContext
from groups.forms import GroupForm, GroupMemberForm, GroupResourceForm
from groups.models import Group, GroupMembership, GroupResource
from updates.models import Incident, Follow
#from groups.signals import CreateGroupMembership
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from accounts.models import SchuleUser
from django.http import HttpResponseNotFound
from django.contrib.contenttypes.models import ContentType
#Group registration
#permission create and check

@login_required
def RegisterGroup(request):
        if request.method =='POST':
                form = GroupForm(request.POST,request.FILES)

                if form.is_valid():
                        newGroup = form.save(commit=False)
                        newGroup.save(user = request.user)

			#No incident to be created here. Add creter to group followers once GroupMembership is updated.

                        return redirect(reverse('group_home', args=(newGroup.id,))) # Redirect after POST
        else:
                form = GroupForm() # An unbound form

        return render_to_response('groups/register.html', {
                'form': form,
        },context_instance=RequestContext(request))


@login_required
def GroupPage(request):
        return render_to_response('groups/groupPage.html',{
        'events':'',
        },context_instance=RequestContext(request))

#decide on membership policy- members only view....or all with restricted access
@login_required
def GroupHome(request,id):
        group = get_object_or_404(Group,pk = id)
        groupAdmin =get_object_or_404(GroupMembership,group__id__exact =id,userType='OW').user

        groupModMembers =[]
        try:
                groupModMembers = GroupMembership.objects.filter(group__id__exact = id,userType="MO")
                #groupMods = [groupMember.user for groupMember in groupWithMods]
        except GroupMembership.DoesNotExist:
                pass
        print "passing to template : " +str(group.id)
        return render_to_response('groups/group.html',{
                'group':group,
                'groupAdmin':groupAdmin,
                'groupMods':groupModMembers,
                })

#decide on permission and execution policy
@login_required
def GroupMember(request,id):
        group = get_object_or_404(Group,pk=id)
        groupMembers = (get_list_or_404(GroupMembership.objects.all().order_by('user'),group__id__exact=id))

        if request.method == 'POST':
                form = GroupMemberForm(request.POST)

                if form.is_valid():
                        new_member = form.save(commit=False)
                        new_member.group = group
                        new_member.save()

			#Create an incident.
			Incidents.objects.create(actor=request.user, action_object=new_member.user, target=group, verb="added")		
			# Add follower to the group.
			group_content = ContentType.objects.get_for_model(Group)
			folo, create = Follo.objects.get_or_create(content_type=group_content, object_id=group.id)
			folo.followers.add(new_member.user)

                        return redirect(reverse('group_member',args=(id,)))
        else:
                form = GroupMemberForm(group_id=id)
        return render_to_response('groups/groupMember.html', {
                        'form': form,
                        'group':group,
                        'groupMembers':groupMembers,
                        },context_instance=RequestContext(request))


#Decide Permission
@login_required
def FlipMembership(request,group_id,user_id):
        group = get_object_or_404(GroupMembership,group__id__exact =group_id,user__id=user_id)
        if(group.userType=='MO'):
                group.userType = 'ST'
        elif(group.userType == 'ST'):
                group.userType = 'MO'
        elif(group.userType=='OW'):
                pass
        else:
                return HttpResponseNotFound("<h1>Not a valid request</h1>")

	#TODO - add notification/alert for the user.

        group.save()
        #respond by redirecting to original page.
        return redirect(reverse('group_member',args=(group_id,)))

        #redirect(request.META.HTTP_REFERER)


@login_required
def UserGroups(request,user_id=None):
        if user_id is None:
                user_id = request.user.id
                user = request.user
        else:
                user = get_object_or_404(SchuleUser,pk=user_id)

        try:
                group_list = user.group_set.all().order_by('-startDate')
        except Group.DoesNotExist:
                group_list =[]

        paginator = Paginator(group_list,5)
        page = request.GET.get('page')

        try:
                groups = paginator.page(page)
        except PageNotAnInteger:
                groups = paginator.page(1)
        except EmptyPage:
                groups = paginator.page(paginator.num_pages)

        return render_to_response('groups/MyGroup.html',{
                'groups':groups,
        },context_instance=RequestContext(request))

@login_required
def AllGroups(request):
        try:
                group_list = Group.objects.all().order_by('-startDate')
        except Group.DoesNotExist:
                group_list =[]

        paginator = Paginator(group_list,5)
        page = request.GET.get('page')

        try:
                groups = paginator.page(page)
        except PageNotAnInteger:
                groups = paginator.page(1)
        except EmptyPage:
                groups = paginator.page(paginator.num_pages)

        return render_to_response('groups/AllGroup.html',{
                'groups':groups,
        },context_instance=RequestContext(request))


@login_required
def RegisterGroupResource(request,group_id):
        group = get_object_or_404(Group,pk=group_id)

        if request.method == 'POST':
                form = GroupResourceForm(request.POST,request.FILES)

                if form.is_valid():
                        res = form.save(commit=False)
                        res.group = group
                        res.save()

			#Create incident.
			Incident.objects.create(actor=request.user, action_object=res, target=group, verb='added')

                        return redirect(reverse('group_resource_page' , args=(group_id, )))

        else:
                form = GroupResourceForm()

        return render_to_response('groups/registerResource.html',{
                'group':group,
                'form':form,
        },context_instance=RequestContext(request))

@login_required
def GroupResourcePage(request,group_id):
        group = get_object_or_404(Group,pk = group_id)
        try:
                res_list = GroupResource.objects.filter(group = group_id).order_by('-date')
        except GroupResource.DoesNotExist:
                res_list = []

        paginator = Paginator(res_list,7)

        page = request.GET.get('page')

        try:
                res = paginator.page(page)
        except PageNotAnInteger:
                res = paginator.page(1)
        except EmptyPage:
                res = paginator.page(paginator.num_pages)

        return render_to_response('groups/groupResource.html',{
                'resources':res,
                'group':group,
        },context_instance=RequestContext(request))


@login_required
def GroupResourceHome(request,group_id,res_id):
        group = get_object_or_404(Group,pk=group_id)

        try:
                res = GroupResource.objects.get(pk=res_id)
        except GroupResource.DoesNotExist:
                res = []

        return render_to_response('groups/groupResourceHome.html',{
                'group':group,
                'resource':res,
                },context_instance=RequestContext(request))

