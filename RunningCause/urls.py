from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'profile.views.users_list', name='home'),

    (r'^account/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    url(r'^account/', include('allauth.urls')),
    url(r'^profile/', include('profile.urls', namespace='profile')),
    url(r'^runs/', include('runs.urls', namespace='runs')),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^wagers/', include('wagers.urls', namespace='wagers')),

    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rosetta/', include('rosetta.urls')),
)
