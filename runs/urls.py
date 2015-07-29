from django.conf.urls import url
from runs import views


urlpatterns = [
    url(r'^user/$', views.user_runs, name='user_runs'),
    url(r'^user/(?P<user_id>\d+)/$', views.user_runs,
        name='user_runs'),
    url(r'^add/$', views.input_run, name='input_run'),
    url(r'^edit/(?P<run_id>\d+)/$', views.edit_run, name='edit_run'),
    url(r'^register-runkeeper/$', views.register_runkeeper,
        name='register_runkeeper'),
]
