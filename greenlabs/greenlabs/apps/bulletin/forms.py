from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')


class ClientForm(UserCreationForm):
    customer = 'CUST'
    executor = 'EXEC'
    admin = 'ADMIN'
    CLIENT_TYPES = (
        (customer, 'customer'),
        (executor, 'executor'),
        (admin, 'admin'),
    )

    type = forms.ChoiceField(choices=CLIENT_TYPES,
                             required=True)

    amount = forms.FloatField(min_value=0)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'type', 'amount')
