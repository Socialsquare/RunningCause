from django.conf.urls import url
from invitations import views

urlpatterns = [
    url(r'^invite-via-email/$', views.invite_via_email,
        name='invite_via_email'),
]
