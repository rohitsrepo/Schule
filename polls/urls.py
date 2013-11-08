from django.conf.url import url,pattern
from polls.views import *

urlpatter = pattern('',
	url(r'^/$','PostsHome'),
	url(r'^post/(?P<post_id>\d+)$','PostHome'),
)
