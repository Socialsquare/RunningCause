from django.conf.urls import url
from challenges import views


urlpatterns = [
    url(r'^feedback/(?P<challenge_id>\d+)/$', views.feedback_challenge,
        name='feedback_challenge'),

    url(r'^invite-sponsor-to-challenge/(?P<person_id>\d+)$',
        views.invite_sponsor_to_challenge,
        name='invite_sponsor_to_challenge'),

    url(r'preview-invitation-challenge/(?P<token>[a-zA-Z0-9\-]{32,36})/$',
        views.preview_invitation_challenge,
        name='preview_invitation_challenge'),

    url(r'^challenge-runner/(?P<person_id>\d+)/$',
        views.challenge_runner,
        name='challenge_runner'),
]
