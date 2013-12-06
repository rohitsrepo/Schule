from django.conf.urls import url,patterns
from forums.views import *

urlpatterns = patterns('forums.views' ,
        url(r'create$','CreateForum',name='course_createForum'),
        url(r'home$','ForumsHome',name='course_forumsHome'),
        url(r'forum/(?P<forum_id>\d+)$','ForumHome',name='course_forumHome'),
	url(r'forum/(?P<forum_id>\d+)/EditForum$','EditForum',name='course_forum_edit'),
)
