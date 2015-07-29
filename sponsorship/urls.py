from django.conf.urls import url

from sponsorship import views


urlpatterns = [
    url(r'^add/(?P<runner_id>\d+)$', views.add_sponsorship,
        name='add_sponsorship'),
    url(r'^end/(?P<sponsorship_id>\d+)/$', views.end_sponsorship,
        name='end_sponsorship'),
    url(r'^request-sponsorship/(?P<person_id>\d+)$', views.request_sponsorship,
        name='request_sponsorship'),
    url(r'^add-sponsorship-from-request/(?P<token>[a-zA-Z0-9\-]{32,36})$',
        views.add_sponsorship_from_request,
        name='add_sponsorship_from_request'),
]
