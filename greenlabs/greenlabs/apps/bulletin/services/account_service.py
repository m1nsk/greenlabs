from ..models import Client, MoneyAccount, Order, Commission
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from ..exceptions.exceptions import SelfOrderException, OrderClosedException


def registration_service(form, request):
    user = form.save()
    amount = form.cleaned_data.get('amount')
    user_type = form.cleaned_data.get('type')
    raw_password = form.cleaned_data.get('password1')
    money_account = MoneyAccount.objects.create(amount=amount)
    Client.objects.create(user=user, money_account=money_account, type=user_type)
    user = authenticate(username=user.username, password=raw_password)
    login(request, user)


def order_list_data_service(request):
    client = Client.objects.get(user=request.user)
    orders = Order.objects.select_related('created_by').filter(status=Order.OPENED)
    context = {
        'order_list': orders,
        'type': client.type
    }
    return context


def profile_data_service(request):
    client = Client.objects.get(user=request.user)
    order_list = Order.objects.filter(created_by=client)
    context = {
        'client': client,
        'order_list': order_list,
        'type': client.type
    }
    return context


def order_creation_service(form, request):
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
    Order.objects.create(created_by=created_by, status=order_status, commission=commission, title=title,
                         description=description, bounty=bounty)


def take_order_service(order_id, request):
    order = get_object_or_404(Order, pk=order_id)
    if order.status == Order.CLOSED:
        raise OrderClosedException
    order.status = Order.CLOSED
    creator = order.created_by
    executor = Client.objects.get(user=request.user)
    if creator.id == executor.id:
        raise SelfOrderException
    order.executed_by = executor
    bounty_count(creator, executor, order)


def bounty_count(creator, executor, order):
    bounty = order.bounty
    bulletin_bounty = bounty * order.commission.value / 100
    executor_bounty = bounty - bulletin_bounty
    creator_account = creator.money_account
    executor_account = executor.money_account
    creator_account.amount -= bounty
    executor_account.amount += executor_bounty
    creator_account.save()
    executor_account.save()
    order.save()


def user_is_executor(user):
    client = Client.objects.get(user=user)
    return client.type == Client.EXECUTOR


def user_is_creator(user):
    client = Client.objects.get(user=user)
    return client.type == Client.CUSTOMER