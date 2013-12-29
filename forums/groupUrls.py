from django.conf.urls import url,patterns

urlpatterns = patterns('forums.groupViews' ,
        url(r'create$','CreateForum',name='group_createForum'),
        url(r'home$','ForumsHome',name='group_forumsHome'),
        url(r'forum/(?P<forum_id>\d+)$','ForumHome',name='group_forumHome'),
	url(r'forum/(?P<forum_id>\d+)/EditForum$','EditForum',name='group_forum_edit'),
)
