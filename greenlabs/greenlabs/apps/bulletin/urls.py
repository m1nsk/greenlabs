from django.conf.urls import url
from .views import login, order_form, order_list

urlpatterns = [
    url(r'^login/$', login),
    url(r'^orders/$', order_list),
    url(r'^orders/form/$', order_form),
]
