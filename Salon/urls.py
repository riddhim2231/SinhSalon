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
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView

from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('appointment_success', TemplateView.as_view(template_name="appointment_success.html"), name="appointment_success"),
    path('login/', my_login, name="login"),
    path('register/', register, name="register"),
    path('dashboard/', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('service/', salon_service, name="service"),
    path('stylists/', get_stylists, name="stylists"),
    path('clients/', get_clients, name="clients"),
    path('appointment_booking/', appointment_booking, name="appointment_booking"),
    path('appointments_list/', get_appointments, name="appointments_list"),
    path('update_appointment_status/', update_appointment_status, name="update_appointment_status"),
    path('logout/', user_logout, name="logout"),
]
