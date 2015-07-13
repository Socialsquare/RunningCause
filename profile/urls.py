from django.conf.urls import patterns, url, include
from profile import views
from django.conf import settings


urlpatterns = patterns('',
    url(r'^my_page/$', views.my_page, name='my_page'),
    url(r'^(?P<user_id>\d+)/$', views.user_view, name='user'),

    url(r'^(?P<user_id>\d+)/raised/$', views.user_raised,
        name='user_raised'),
    url(r'^(?P<user_id>\d+)/donated/$', views.user_donated,
        name='user_donated'),
    url(r'^/settings/$', views.user_settings, name='user_settings'),
    url(r'^/unregister/$', views.unregister_card, name='unregister'),
    url(r'^info_widget/$', views.info_widget, name='info_widget'),
    url(r'^makepublic/$', views.make_profile_public,
        name='make_profile_public'),
    url(r'^makeprivate/$', views.make_profile_private,
        name='make_profile_private'),
    url(r'^register_customer/$', views.register_customer,
        name='register_customer'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^signuporlogin/$', views.signup_or_login, name='signup_or_login'),
    url(r'^credit_card_prompt/$', views.credit_card_prompt,
        name='credit_card_prompt'),
    url(r'^sign_in_landing/$', views.sign_in_landing, name='sign_in_landing'),
)
