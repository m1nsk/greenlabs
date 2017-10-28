from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm, OrderForm
from .models import Client, MoneyAccount, Order, Commission
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.http import Http404


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
    try:
        with transaction.atomic():
            client = Client.objects.get(user=request.user)
            orders = Order.objects.select_related('created_by').filter(status=Order.OPENED).exclude(created_by=client)
            context = {
                'order_list': orders,
                'type': client.type
            }
            return render(request, 'order_list.html', context)
    except IntegrityError:
        raise Http404


@login_required
def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    created_by = Client.objects.get(user=request.user)
                    commission_value = 10
                    commission, created = Commission.objects.get_or_create(
                        id=1,
                        defaults={'value': commission_value}
                    )
                    order_status = Order.OPENED
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
    return render(request, 'order_form.html', {'form': form})


@login_required
def take_order(request, order_id):
    if request.method == 'GET':
        try:
            with transaction.atomic():
                order = get_object_or_404(Order, pk=order_id)
                if order.status == Order.CLOSED:
                    return redirect('order_closed')
                order.status = Order.CLOSED
                creator = order.created_by
                executor = Client.objects.get(user=request.user)
                if creator.id == executor.id:
                    return redirect('order_forbidden')
                order.executed_by = executor
                creator_account, executor_account = change_money_accounts(creator, executor, order)
                creator_account.save()
                executor_account.save()
                order.save()
        except IntegrityError:
            raise Http404
        else:
            return redirect('order_list')


def change_money_accounts(creator, executor, order):
    bounty = order.bounty
    bulletin_bounty = bounty * order.commission.value / 100
    executor_bounty = bounty - bulletin_bounty
    creator_account = creator.money_account
    executor_account = executor.money_account
    creator_account.amount -= bounty
    executor_account.amount += executor_bounty
    return creator_account, executor_account


@login_required
def order_closed(request):
    return render(request, 'order_closed.html')


@login_required
def order_forbidden(request):
    return render(request, 'order_forbidden.html')


@login_required
def profile(request):
    try:
        with transaction.atomic():
            client = Client.objects.get(user=request.user)
            order_list = Order.objects.filter(created_by=client)
            context = {
                'client': client,
                'order_list': order_list,
                'type': client.type
            }
            return render(request, 'profile.html', context)
    except IntegrityError:
        raise Http404
