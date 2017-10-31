from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import OrderFormView, OrderListView, RegistrationView, OrderClosedVIew, OrderForbiddenView, ProfileView, TakeOrderView

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html',
         'redirect_field_name': 'next'},
        name='login'
        ),
    url(r'^logout/$', auth_views.logout,
        {'next_page': 'login'},
        name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^orders/$', OrderListView.as_view(), name='order_list'),
    url(r'^orders/(?P<order_id>\d+)$', TakeOrderView.as_view(), name='take_order'),
    url(r'^orders/form/$', OrderFormView.as_view(), name='order_form'),
    url(r'^orders/closed/$', OrderClosedVIew.as_view(), name='order_closed'),
    url(r'^orders/forbidden/$', OrderForbiddenView.as_view(), name='order_forbidden'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]
