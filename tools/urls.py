from django.conf.urls import url

from tools import views


urlpatterns = [
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^payments/$', views.payments, name='payments'),
    url(r'^payments/(?P<user_id>\d+)/$', views.payment_transactions, name='payment_transactions'),
    url(r'^info_widget/$', views.info_widget, name='info_widget'),
    url(r'^charge-all-users/$', views.charge_all_users,
        name='charge_all_users'),
    url(r'^charge-user/(?P<user_id>\d+)/$', views.charge_user, name='charge_user'),
]
