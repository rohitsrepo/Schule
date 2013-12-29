from django.conf.urls import url,patterns

urlpatterns = patterns('polls.groupViews' ,
        url(r'create$','CreatePoll',name='group_createPoll'),
        url(r'home$','PollsHome',name='group_pollsHome'),
        url(r'poll/(?P<poll_id>\d+)$','PollHome',name='group_pollHome'),
        url(r'poll/(?P<poll_id>\d+)/status$','PollStatus',name='group_pollStatus'),
        url(r'poll/(?P<poll_id>\d+)/AddOptions$','CreatePollOption',name='group_poll_op'),
        url(r'poll/(?P<poll_id>\d+)/EditPoll$','EditPoll',name='group_poll_edit'),
)

