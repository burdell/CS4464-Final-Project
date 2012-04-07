from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'index.html'}),
    (r'^register/$', 'map.views.register'),
    (r'^accounts/login/$', 'login'),
    (r'^accounts/logout/$', 'logout'),
)
