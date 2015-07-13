from django.conf.urls import patterns, url, include
from wagers import views
from django.conf import settings


urlpatterns = patterns('',
    url(r'^(?P<sponsee_id>\d+)/make_wager/$', views.make_wager, name='wager'),
    url(r'^(?P<wager_id>\d+)/update_wager/$', views.update_wager, name='update_wager'),
    url(r'^(?P<wager_id>\d+)/confirm_wager/$', views.confirm_wager, name='confirm_wager'),
    url(r'^(?P<wager_id>\d+)/decline_wager/$', views.decline_wager, name='decline_wager'),
    url(r'^(?P<sponsee_id>\d+)/make_wager/(?P<wager_id>\d+)/$', views.make_wager, name='wager_from_invite'),
    url(r'^(?P<sponsor_id>\d+)/invite_wager/$', views.invite_wager, name='invite_wager'),
)
