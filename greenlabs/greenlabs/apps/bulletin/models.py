from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Commission(models.Model):
    value = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return str(self.value)


class MoneyAccount(models.Model):
    amount = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

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
        return str(self.user.username)


class Order(models.Model):
    OPENED = 'OP'
    CLOSED = 'CL'
    order_status = (
        (OPENED, 'opened'),
        (CLOSED, 'closed')
    )
    created_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='customer')
    bounty = models.FloatField(default=0)
    title = models.CharField(default='', max_length=25)
    description = models.TextField(default='',)
    status = models.CharField(max_length=2,
                            choices=order_status,
                            blank=False,
                            default=CLOSED)
    executed_by = models.ForeignKey(Client, related_name='executor', null=True, blank=True)
    commission = models.ForeignKey(Commission)

    def __str__(self):
        return str(self.title)
