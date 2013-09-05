from django.conf.urls import patterns, include, url
from accounts import urls as accountUrls
from django.conf import settings
from django.views.generic import TemplateView
#from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^$', 'schule.views.home', name='home'),
    # url(r'^schule/', include('schule.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^schule_name/$', TemplateView.as_view(template_name='base.html'),name='home'),	
    url(r'schule_name/accounts/',include(accountUrls)),
)
