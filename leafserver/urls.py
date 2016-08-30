from django.conf.urls import patterns, include, url
from django.contrib import admin

import dashboard
from views import IndexView, LoginView


dashboard_urlpatterns = patterns('',
    url(r'^$', dashboard.Index.as_view()),
    url(r'^home_config/$', dashboard.HomeConfig.as_view()),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leafautumn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view()),
    url(r'^account/login/$', LoginView.as_view()),
    url(r'^dashboard/', include(dashboard_urlpatterns)),
)
