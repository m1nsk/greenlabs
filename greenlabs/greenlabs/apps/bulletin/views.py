from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def registration(request):
    return HttpResponse('registration')


def login(request):
    return HttpResponse('login')


def order_list(request):
    return HttpResponse('order_list')


def order_form(request):
    return HttpResponse('order_form')