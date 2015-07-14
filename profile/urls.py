from django.conf.urls import url
from profile import views


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.user_page, name='user_page'),
    url(r'^my-page/$', views.my_page, name='my_page'),
    url(r'^users-list/$', views.users_list, name='users_list'),
    url(r'^(?P<user_id>\d+)/raised/$', views.user_raised,
        name='user_raised'),
    url(r'^(?P<user_id>\d+)/donated/$', views.user_donated,
        name='user_donated'),
    url(r'^settings/$', views.user_settings, name='user_settings'),
    url(r'^unregister/$', views.unregister_card, name='unregister'),
    url(r'^makepublic/$', views.make_profile_public,
        name='make_profile_public'),
    url(r'^makeprivate/$', views.make_profile_private,
        name='make_profile_private'),
    url(r'^register_customer/$', views.register_customer,
        name='register_customer'),
    url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^signuporlogin/$', views.signup_or_login, name='signup_or_login'),
    url(r'^credit_card_prompt/$', views.credit_card_prompt,
        name='credit_card_prompt'),
    url(r'^sign_in_landing/$', views.sign_in_landing, name='sign_in_landing'),
]
