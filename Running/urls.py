from django.conf.urls import patterns, url, include
from Running import views

urlpatterns = patterns('',
    # url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    (r'^account/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^account/', include('allauth.urls')),
    url(r'^(?P<runner_id>\S+)/profile/$', views.user, name='user'),
    url(r'^(?P<runner_id>\S+)/input_run/$', views.input_run, name='input'),
    url(r'^(?P<sponsee_id>\S+)/sponsor/$', views.sponsor, name='sponsor'),
    url(r'^(?P<runner_id>\S+)/register/runkeeper/$', views.register_runkeeper, name='register_runkeeper'),
    url(r'^(?P<sponsorship_id>\S+)/deletesponsorship/(?P<runner_id>\S+)/$', views.delete_sponsorship, name='delete_sponsorship'),
    url(r'^$', views.home, name='home'),
)