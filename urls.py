from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'index.html'}),
     (r'^admin/', include(admin.site.urls)),
    (r'^register/$', 'map.views.register'),
    url(r'^accounts/login/$', login, {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'index.html'}),
    url(r'^map_page/post/', 'map.views.map_post'),
    url(r'^map_page/$', 'map.views.map_page'), 
)
