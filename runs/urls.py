from django.conf.urls import patterns, url, include
from runs import views
from django.conf import settings


urlpatterns = patterns('',
    url(r'^user/$', views.user_runs, name='user_runs'),
    url(r'^user/(?P<user_id>\d+)/$', views.user_runs,
        name='user_runs'),
    url(r'^add/$', views.input_run, name='input_run'),
    url(r'^edit/(?P<run_id>\d+)/$', views.edit_run, name='edit_run'),
    url(r'^(?P<runner_id>\d+)/register/runkeeper/$', views.register_runkeeper,
        name='register_runkeeper'),
)