from django.conf.urls import url
from .views import why_join_us, frontpage

urlpatterns = [
    url(r'^$', frontpage, name='frontpage'),
    url(r'^why-join-us/$', why_join_us, name='why_join_us')
]
