from django.conf.urls import include,patterns,url
from django.conf import settings
from polls import urls as polls_urls

urlpatterns = patterns('courses.views',
    url(r'RegisterCourse/$','RegisterCourse',name="register_course_url"),
    url(r'course/(?P<id>\d+)/$','CourseHome',name="course_home_url"),
    url(r'course/(?P<id>\d+)/members/$','CourseMember',name="course_member_url"),
    url(r'course/(?P<course_id>\d+)/flipMembership/(?P<user_id>\d+)/$','FlipMembership',name="flip_course_membership"),
    #url(r'^course/(?P<id>\d+)/posts$','CoursePosts',name="course_posts_url"),
)

urlpatterns += patterns('',
    url(r'course/(?P<course_id>\d+)/polls/',include(polls_urls)),
)
