from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def login(request):
    return HttpResponse('login')


def order_list(request):
    return HttpResponse('order_list')


def order_form(request):
    return HttpResponse('order_form')