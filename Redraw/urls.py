"""Redraw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import django_cas_ng.views
from django.views.generic.base import RedirectView
from RedrawApp import api

favicon_view = RedirectView.as_view(url='../build/redraw.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^favicon.ico$', favicon_view),
    re_path('^$', django_cas_ng.views.login, name='cas_ng_login'),
    re_path('^accounts/logout$', django_cas_ng.views.logout, name='cas_ng_logout'),
    re_path('^accounts/callback$', django_cas_ng.views.callback, name='cas_ng_callback'),
    re_path('^api/search/', api.query, name = "query"),
    re_path('^api/floorplan/', api.get_floorplan, name='floorplan'),
    re_path('^api/favorites/', api.favorites, name="favorites"),
    re_path('.*', login_required(TemplateView.as_view(template_name='index.html'))),
]


