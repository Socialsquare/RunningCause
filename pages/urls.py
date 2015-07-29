from django.conf.urls import url
from .views import why_join_us

urlpatterns = [
    url(r'^why-join-us/$', why_join_us,
        name='why_join_us'),
]
