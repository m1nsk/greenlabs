from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import ClientForm
from .models import Client, MoneyAccount
from django.db import IntegrityError, transaction
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
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
                    return redirect('order_list')
            except IntegrityError:
                raise Http404
    else:
        form = ClientForm
    return render(request, 'registration.html', {'form': form})


class UserLogin(FormView):
    form_class = AuthenticationForm

    template_name = "login.html"

    success_url = "/bulletin/orders"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(UserLogin, self).form_valid(form)


def order_list(request):
    print(request.user.username, '2111111111111111111111111111111111111')
    return HttpResponse('order_list')


def order_form(request):
    return HttpResponse('order_form')