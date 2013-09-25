from django.conf.urls import patterns,url
from django.conf import settings

urlpatterns = patterns('courses.views',
    url(r'^RegisterCourse/','RegisterCourse',name="register_course_url"),
    url(r'^course/(?P<id>\d+)','CourseHome',name="course_home_url"),
    url(r'^course/(?P<id>\d+)/members','CourseMember',name="course_member_url"),

)
