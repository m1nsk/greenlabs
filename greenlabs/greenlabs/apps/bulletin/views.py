from django.shortcuts import redirect
from .exceptions.exceptions import SelfOrderException, OrderClosedException
from .forms import ClientForm, OrderForm
from .models import Client, Order
from .services.account_service import registration_service, order_creation_service, take_order_service, user_is_creator, user_is_executor
from django.db import transaction
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = ClientForm

    def form_valid(self, form):
        with transaction.atomic():
            registration_service(form, self.request)
        return redirect('order_list')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.select_related('created_by').filter(status=Order.OPENED)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['type'] = self.request.user.client.type
        return context


class OrderFormView(UserPassesTestMixin, LoginRequiredMixin, FormView):
    def test_func(self):
        return user_is_creator(self.request.user)

    template_name = 'order_form.html'
    form_class = OrderForm

    def form_valid(self, form):
        with transaction.atomic():
            order_creation_service(form, self.request)
        return redirect('order_list')


class TakeOrderView(UserPassesTestMixin, LoginRequiredMixin, RedirectView):
    def test_func(self):
        return user_is_executor(self.request.user)

    def get_redirect_url(self, *args, **kwargs):
        with transaction.atomic():
            try:
                take_order_service(self.kwargs['order_id'], self.request)
            except OrderClosedException:
                return reverse('order_closed')
            except SelfOrderException:
                return reverse('order_forbidden')
        return reverse('order_list')


class ProfileView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user.client

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        client = self.request.user.client
        context['order_list'] = Order.objects.filter(created_by=client)
        context['type'] = client.type
        return context


class OrderForbiddenView(LoginRequiredMixin, TemplateView):
    template_name = 'message_page.html'

    def get_context_data(self, **kwargs):
        context = {
            'message': 'It seems to be like you are trying to take your own order. Sorry, but this action is forbidden'
        }
        return context


class OrderClosedVIew(LoginRequiredMixin, TemplateView):
    template_name = 'message_page.html'

    def get_context_data(self, **kwargs):
        context = {
            'message': 'Sorry, but order has been closed. Click redirect button to see updated order list'
        }
        return context

