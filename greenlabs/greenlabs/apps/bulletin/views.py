from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, OrderForm
from .models import Client, MoneyAccount, Order, Commission
from django.db import IntegrityError, transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic.edit import FormView

# Create your views here.


def registration(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    user.refresh_from_db()
                    amount = form.cleaned_data.get('amount')
                    user_type = form.cleaned_data.get('type')
                    money_account = MoneyAccount.objects.create(amount=amount)
                    Client.objects.create(user=user, money_account=money_account, type=user_type)
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=user.username, password=raw_password)
                    login(request, user)
            except IntegrityError:
                raise Http404
            else:
                return redirect('order_list')
    else:
        form = ClientForm
    return render(request, 'registration.html', {'form': form})


@login_required
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(status='OP')
        context = {
            'order_list': orders
        }
        print(context)
        return render(request, 'order_list.html', context)


@login_required
def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.get(id=request.user.id)
                    created_by = Client.objects.get(user=user.id)
                    commission_value = 10
                    commission, created = Commission.objects.get_or_create(
                        id=1,
                        defaults={'value': commission_value}
                    )
                    order_status = 'OP'
                    title = form.cleaned_data.get('title')
                    description = form.cleaned_data.get('description')
                    bounty = form.cleaned_data.get('bounty')
                    Order.objects.create(created_by=created_by, status=order_status, commission=commission, title=title, description=description, bounty=bounty)
            except IntegrityError:
                raise Http404
            else:
                return redirect('order_list')
    else:
        form = OrderForm
    return render(request, 'registration.html', {'form': form})


@login_required
def take_order(request, order_id):
    if request.method == 'GET':
        try:
            with transaction.atomic():
                order = get_object_or_404(Order, pk=order_id)
                if order.status == 'CL':
                    redirect('order_closed')
                order.status = 'CL'
                print(request.user.id)
                user = User.objects.get(id=request.user.id)
                executed_by = Client.objects.get(user=user)
                order.executed_by = executed_by
                order.save()
        except IntegrityError:
            raise Http404
        else:
            return redirect('order_list')


@login_required
def order_closed(request):
    return render(request, 'order_closed.html')