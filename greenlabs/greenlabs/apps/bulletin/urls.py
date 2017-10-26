from django.conf.urls import url
from .views import UserLogin, order_form, order_list, registration, logout_view

urlpatterns = [
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^orders/$', order_list, name='order_list'),
    url(r'^orders/form/$', order_form, name='order_form'),
]
