from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import IndexView, LoginView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leafautumn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view()),
    url(r'^account/login/$', LoginView.as_view()),
)
