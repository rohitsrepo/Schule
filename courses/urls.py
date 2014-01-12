from django.conf.urls import include,patterns,url
from django.conf import settings
from polls import courseUrls as poll_urls
from forums import courseUrls as forum_urls

urlpatterns = patterns('courses.views',
    url(r'RegisterCourse$','RegisterCourse',name="register_course"),
    url(r'course/(?P<id>\d+)$','CourseHome',name="course_home"),
    url(r'course/(?P<id>\d+)/updates$','CourseUpdates',name="course_updates"),
    url(r'course/(?P<id>\d+)/members$','CourseMember',name="course_member"),
    url(r'course/(?P<course_id>\d+)/flipMembership/(?P<user_id>\d+)$','FlipMembership',name="flip_course_membership"),
    url(r'MyCourses$','UserCourses',name='my_course'),
    url(r'UserCourses/(?P<user_id>\d+)$','UserCourses',name='user_course'),
    url(r'AllCourses$','AllCourses',name='all_course'),
    url(r'course/(?P<course_id>\d+)/resources/register$','RegisterCourseResource',name="register_course_resource"),
    url(r'course/(?P<course_id>\d+)/resources$','CourseResourcePage',name="course_resource_page"),
    url(r'course/(?P<course_id>\d+)/resources/(?P<res_id>\d+)/$','CourseResourceHome',name='course_resource_home'),
    url(r'/$','CoursePage',name="course_page"),

    #url(r'^course/(?P<id>\d+)/posts$','CoursePosts',name="course_posts_url"),
)

urlpatterns += patterns('',
    url(r'course/(?P<course_id>\d+)/polls/',include(poll_urls)),
    url(r'course/(?P<course_id>\d+)/forums/',include(forum_urls)),
)
