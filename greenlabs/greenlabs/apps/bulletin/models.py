from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class Commission(models.Model):
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)


class MoneyAccount(models.Model):
    amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.amount)


class Client(models.Model):
    customer = 'CUST'
    executor = 'EXEC'
    admin = 'ADMIN'
    CLIENT_TYPES = (
        (customer, 'customer'),
        (executor, 'executor'),
        (admin, 'admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=4,
                            blank=False,
                            choices=CLIENT_TYPES,
                            default=customer)
    money_account = models.ForeignKey(MoneyAccount, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    open = 'OP'
    closed = 'CL'
    order_status = (
        (open, 'open'),
        (closed, 'closed')
    )
    created_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='customer')
    bounty = models.FloatField(default=0)
    title = models.CharField(default='', max_length=25)
    description = models.TextField(default='',)
    type = models.CharField(max_length=2,
                            choices=order_status,
                            blank=False,
                            default=closed)
    executed_by = models.ForeignKey(Client, related_name='executor')
    commission = models.ForeignKey(Commission)

    def __str__(self):
        return str(self.title)
