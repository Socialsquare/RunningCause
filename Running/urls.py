from django.conf.urls import patterns, url, include
from Running import views
from Running.views import runs as views_runs
from Running.views import wagers as views_wagers
from django.conf import settings


urlpatterns = patterns('',
    (r'^account/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^account/', include('allauth.urls')),
    url(r'^my_page/$', views.my_page, name='my_page'),
    url(r'^(?P<user_id>\d+)/profile/$', views.user_view, name='user'),

    url(r'^(?P<user_id>\d+)/profile/raised/$', views.user_raised,
        name='user_raised'),
    url(r'^(?P<user_id>\d+)/profile/donated/$', views.user_donated,
        name='user_donated'),
    url(r'^profile/settings/$', views.user_settings, name='user_settings'),
    url(r'^/unregister/$', views.unregister_card, name='unregister'),
    url(r'^info_widget/$', views.info_widget, name='info_widget'),

    url(r'^runs/user/$', views_runs.user_runs, name='user_runs'),
    url(r'^runs/user/(?P<user_id>\d+)/$', views_runs.user_runs,
        name='user_runs'),
    url(r'^runs/add/$', views_runs.input_run, name='input_run'),
    url(r'^runs/edit/(?P<run_id>\d+)/$', views_runs.edit_run, name='edit_run'),

    url(r'^(?P<sponsee_id>\d+)/make_wager/$', views_wagers.make_wager, name='wager'),
    url(r'^(?P<wager_id>\d+)/update_wager/$', views_wagers.update_wager, name='update_wager'),
    url(r'^(?P<wager_id>\d+)/confirm_wager/$', views_wagers.confirm_wager, name='confirm_wager'),
    url(r'^(?P<wager_id>\d+)/decline_wager/$', views_wagers.decline_wager, name='decline_wager'),
    url(r'^(?P<sponsee_id>\d+)/make_wager/(?P<wager_id>\d+)/$', views_wagers.make_wager, name='wager_from_invite'),
    url(r'^(?P<sponsor_id>\d+)/invite_wager/$', views_wagers.invite_wager, name='invite_wager'),

    url(r'^sponsorship/add/(?P<runner_id>\d+)$', views.add_sponsorship,
        name='add_sponsorship'),

    url(r'^(?P<sponsor_id>\d+)/invite/$', views.invite_sponsor, name='invite_sponsor'),
    url(r'^invite_from_email/$', views.invite_sponsor, name='invite_from_email'),
    url(r'^(?P<runner_id>\d+)/register/runkeeper/$', views.register_runkeeper, name='register_runkeeper'),
    url(r'^(?P<sponsorship_id>\d+)/endsponsorship/$', views.end_sponsorship, name='end_sponsorship'),
    url(r'^profile/makepublic/$', views.make_profile_public, name='make_profile_public'),
    url(r'^profile/makeprivate/$', views.make_profile_private, name='make_profile_private'),
    url(r'^register_customer/$', views.register_customer, name='register_customer'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^signuporlogin/$', views.signup_or_login, name='signup_or_login'),
    url(r'^credit_card_prompt/$', views.credit_card_prompt, name='credit_card_prompt'),
    url(r'^sign_in_landing/$', views.sign_in_landing, name='sign_in_landing'),
    url(r'^$', views.home, name='home'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
        )