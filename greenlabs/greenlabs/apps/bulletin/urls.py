from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import order_form, order_list, registration, take_order, order_closed, order_forbidden, profile

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html',
         'redirect_field_name': 'next'},
        name='login'
        ),
    url(r'^logout/$', auth_views.logout,
        {'next_page': 'login'},
        name='logout'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^orders/$', order_list, name='order_list'),
    url(r'^orders/(?P<order_id>\d+)$', take_order, name='take_order'),
    url(r'^orders/form/$', order_form, name='order_form'),
    url(r'^orders/closed/$', order_closed, name='order_closed'),
    url(r'^orders/forbidden/$', order_forbidden, name='order_forbidden'),
    url(r'^profile/$', profile, name='profile'),
]
