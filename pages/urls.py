from django.conf.urls import url
from .views import contact, frontpage

urlpatterns = [
    url(r'^$', frontpage, name='frontpage'),
    url(r'^contact/$', contact, name='contact')
]
