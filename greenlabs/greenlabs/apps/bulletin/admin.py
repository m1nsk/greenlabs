from django.contrib import admin
from .models import Commission, MoneyAccount, Order, Client


class CommissionInline(admin.StackedInline):
    model = Commission


class OrderInline(admin.TabularInline):
    model = Order
    fk_name = 'created_by'


class ClientInline(admin.StackedInline):
    model = Client


class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'bounty', 'title', 'description', 'status', 'executed_by', 'commission']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'money_account', 'user']


class CommissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


class MoneyAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount']


admin.site.register(Commission, CommissionAdmin)
admin.site.register(MoneyAccount, MoneyAccountAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
