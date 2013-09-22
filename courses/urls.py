from django.conf.urls import patterns,url
from django.conf import settings

urlpatterns = patterns('courses.views',
    url(r'^registerCourse/','registerCourse',name="register_course_url"),
)
