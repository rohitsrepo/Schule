from django.conf.urls import url,patterns
from polls.views import *

urlpatterns = patterns('polls.views' ,
	url(r'create$','CreatePoll',name='course_createPoll'),
	url(r'home$','PollsHome',name='course_pollsHome'),
	url(r'poll/(?P<poll_id>\d+)$','PollHome',name='course_pollHome'),
	url(r'poll/(?P<poll_id>\d+)/status$','PollStatus',name='course_pollStatus'),
	url(r'poll/(?P<poll_id>\d+)/AddOptions$','CreatePollOption',name='course_poll_op'),
	url(r'poll/(?P<poll_id>\d+)/EditPoll$','EditPoll',name='course_poll_edit'),
)
