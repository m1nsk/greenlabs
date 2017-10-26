from django.contrib import admin
from .models import Commission, MoneyAccount, Order, Client


class OrderInline(admin.StackedInline):
    model = Order


class ClientInline(admin.StackedInline):
    model = Client


class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'bounty', 'title', 'description', 'type', 'executed_by', 'commission']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'money_account']
    inlines = [
        OrderInline
    ]


class CommissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    inlines = [
        OrderInline
    ]


class MoneyAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount']
    inlines = [
        ClientInline
    ]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(MoneyAccount, MoneyAccountAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
