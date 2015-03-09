from django.conf.urls import patterns, url, include
from Running import views
from django.conf import settings

urlpatterns = patterns('',
    (r'^account/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    (r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^account/', include('allauth.urls')),
    url(r'^my_page/$', views.my_page, name='my_page'),
    url(r'^(?P<user_id>\S+)/profile/$', views.user, name='user'),
    url(r'^(?P<runner_id>\S+)/input_run/$', views.input_run, name='input'),
    url(r'^(?P<run_id>\S+)/edit_run/$', views.edit_run, name='edit'),
    url(r'^(?P<sponsee_id>\S+)/sponsor/$', views.sponsor, name='sponsor'),
    url(r'^(?P<sponsee_id>\S+)/sponsor/(?P<sponsorship_id>\S+)/$', views.sponsor, name='sponsor_from_invite'),
    url(r'^(?P<sponsor_id>\S+)/invite/$', views.invite_sponsor, name='invite_sponsor'),
    url(r'^invite_from_email/$', views.invite_sponsor, name='invite_from_email'),
    url(r'^(?P<runner_id>\S+)/register/runkeeper/$', views.register_runkeeper, name='register_runkeeper'),
    url(r'^(?P<sponsorship_id>\S+)/endsponsorship/(?P<runner_id>\S+)/$', views.end_sponsorship, name='end_sponsorship'),
    url(r'^(?P<user_id>\S+)/makeuserpublic/$', views.make_user_public, name='make_user_public'),
    url(r'^(?P<user_id>\S+)/makeuserprivate/$', views.make_user_private, name='make_user_private'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^signuporlogin/$', views.signup_or_login, name='signup_or_login'),
    url(r'^$', views.home, name='home'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
        )