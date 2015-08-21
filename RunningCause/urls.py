from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='pages:why_join_us'),
        name='home'),

    url(r'^account/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    url(r'^account/', include('allauth.urls')),
    url(r'^profile/', include('profile.urls', namespace='profile')),
    url(r'^runs/', include('runs.urls', namespace='runs')),
    url(r'^invitations/', include('invitations.urls',
                                  namespace='invitations')),
    url(r'^challenges/', include('challenges.urls', namespace='challenges')),
    url(r'^sponsorship/', include('sponsorship.urls',
                                  namespace='sponsorship')),
    url(r'^tools/', include('tools.urls', namespace='tools')),
    url(r'^pages/', include('pages.urls', namespace='pages')),
    url(r'^info_widget/',
        RedirectView.as_view(pattern_name='tools:info_widget')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rosetta/', include('rosetta.urls')),
]
