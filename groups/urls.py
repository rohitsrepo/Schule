from django.conf.urls import include,patterns,url
from django.conf import settings
from polls import groupUrls as polls_urls
from forums import groupUrls as forums_urls

urlpatterns = patterns('groups.views',
    url(r'RegisterGroup$','RegisterGroup',name="register_group"),
    url(r'group/(?P<id>\d+)$','GroupHome',name="group_home"),
    url(r'group/(?P<id>\d+)/members$','GroupMember',name="group_member"),
    url(r'group/(?P<group_id>\d+)/flipMembership/(?P<user_id>\d+)$','FlipMembership',name="flip_group_membership"),
    url(r'MyGroups$','UserGroups',name='my_group'),
    url(r'UserGroups/(?P<user_id>\d+)$','UserGroups',name='user_group'),
    url(r'AllGroups$','AllGroups',name='all_group'),
    url(r'group/(?P<group_id>\d+)/resources/register$','RegisterGroupResource',name="register_group_resource"),
    url(r'group/(?P<group_id>\d+)/resources$','GroupResourcePage',name="group_resource_page"),
    url(r'group/(?P<group_id>\d+)/resources/(?P<res_id>\d+)/$','GroupResourceHome',name='group_resource_home'),
    url(r'/$','GroupPage',name="group_page"),

    #url(r'^group/(?P<id>\d+)/posts$','GroupPosts',name="group_posts_url"),
)

urlpatterns += patterns('',
    url(r'group/(?P<group_id>\d+)/polls/',include(polls_urls)),
    url(r'group/(?P<group_id>\d+)/forums/',include(forums_urls)),
)

