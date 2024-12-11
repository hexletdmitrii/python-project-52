from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


def index(request):
    return HttpResponse('Привет мир')


class HomeView(TemplateView):
    template_name = "home.html"
