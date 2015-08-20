from django.conf.urls import url

from tools import views


urlpatterns = [
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^info_widget/$', views.info_widget, name='info_widget'),
    url(r'^charge-users-now/$', views.charge_users_now,
        name='charge_users_now'),
]