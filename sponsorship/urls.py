from django.conf.urls import url

from sponsorship import views


urlpatterns = [
    url(r'^add/(?P<runner_id>\d+)$', views.add_sponsorship,
        name='add_sponsorship'),
    url(r'^(?P<sponsor_id>\d+)/request/$', views.request_sponsorship,
        name='request_sponsorship'),
    url(r'^(?P<sponsorship_id>\d+)/end/$', views.end_sponsorship,
        name='end_sponsorship'),
]
