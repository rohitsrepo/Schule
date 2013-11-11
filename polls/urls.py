from django.conf.urls import url,patterns
from polls.views import *

urlpatterns = patterns('polls.views' ,
	url(r'create$','CreatePoll',name='createPoll'),
	url(r'home$','PollsHome',name='pollsHome'),
	url(r'poll/(?P<poll_id>\d+)$','PollHome',name='pollHome'),
	url(r'poll/(?P<poll_id>\d+)/status$','PollStatus',name='pollStatus'),

)
