from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse


def cadastro(request):
    return HttpResponse('cadastro')

def login(request):
    return HttpResponse('login')
