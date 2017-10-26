from __future__ import unicode_literals

from django.db import models


class Commission(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.comission)


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
    name = models.CharField(max_length=25)
    type = models.CharField(max_length=4,
                            choices=CLIENT_TYPES,
                            default=customer)
    money_account = models.ForeignKey(MoneyAccount, on_delete=models.CASCADE)


class Order(models.Model):
    open = 'OP'
    closed = 'CL'
    order_status = (
        (open, 'open'),
        (closed, 'closed')
    )
    created_by = models.ForeignKey(Client, on_delete=models.CASCADE)
    bounty = models.FloatField(default=0)
    title = models.CharField(default='', max_length=25)
    description = models.TextField(default='',)
    type = models.CharField(max_length=2,
                            choices=order_status,
                            default=closed)
    created_by = models.ForeignKey(Client)
    commission = models.ForeignKey(Commission)
