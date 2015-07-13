from django.conf.urls import patterns, url, include
from Running import views
from Running.views import runs as views_runs
from Running.views import wagers as views_wagers
from django.conf import settings


urlpatterns = patterns('',
    url(r'^invite_via_email/$', views.invite_via_email,
        name='invite_via_email'),
)