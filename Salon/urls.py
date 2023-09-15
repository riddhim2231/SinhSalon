"""Salon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from accounts.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^appointment_success$', TemplateView.as_view(template_name="appointment_success.html"), name="appointment_success"),
    url(r'^login/$', my_login, name="login"),
    url(r'^register/$', register, name="register"),
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^service/$', salon_service, name="service"),
    url(r'^stylists/$', get_stylists, name="stylists"),
    url(r'^clients/$', get_clients, name="clients"),
    url(r'^appointment_booking/$', appointment_booking, name="appointment_booking"),
    url(r'^appointments_list/$', get_appointments, name="appointments_list"),
    url(r'^update_appointment_status/$', update_appointment_status, name="update_appointment_status"),
    url(r'^logout/$', user_logout, name="logout"),
]
