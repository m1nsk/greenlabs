from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .exceptions.exceptions import SelfOrderException, OrderClosedException
from .forms import ClientForm, OrderForm
from .models import Client, MoneyAccount, Order, Commission
from .services.account_service import registration_service, order_list_data_service, order_creation_service, take_order_service, profile_data_service, user_is_creator, user_is_executor
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404


def registration(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    registration_service(form, request)
            except IntegrityError:
                raise Http404
            else:
                return redirect('order_list')
    else:
        form = ClientForm
    return render(request, 'registration.html', {'form': form})


@login_required
def order_list(request):
    try:
        with transaction.atomic():
            context = order_list_data_service(request)
            return render(request, 'order_list.html', context)
    except IntegrityError:
        raise Http404


@login_required
@user_passes_test(user_is_creator)
def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order_creation_service(form, request)
            except IntegrityError:
                raise Http404
            else:
                return redirect('order_list')
    else:
        form = OrderForm
    return render(request, 'order_form.html', {'form': form})


@login_required
@user_passes_test(user_is_executor)
def take_order(request, order_id):
    if request.method == 'GET':
        try:
            with transaction.atomic():
                try:
                    take_order_service(order_id, request)
                except OrderClosedException:
                    return redirect('order_closed')
                except SelfOrderException:
                    return redirect('order_forbidden')
        except IntegrityError:
            raise Http404
        else:
            return redirect('order_list')


@login_required
def order_closed(request):
    context = {
        'message': 'Sorry, but order has been closed. Click redirect button to see updated order list'
    }
    return render(request, 'message_page.html', context)


@login_required
def order_forbidden(request):
    context = {
        'message': 'It seems to be like you are trying to take your own order. Sorry, but this action is forbidden'
    }
    return render(request, 'message_page.html', context)


@login_required
def profile(request):
    try:
        with transaction.atomic():
            context = profile_data_service(request)
            return render(request, 'profile.html', context)
    except IntegrityError:
        raise Http404



