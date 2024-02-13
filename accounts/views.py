# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth import login as auth_login
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import datetime

from .forms import *

import json

def my_login(request):
    form = LoginForm(request.POST or None)
    template_name = 'login.html'

    if request.method == 'POST':
        if form.is_valid():
            print("email",form.data['email'])
            print("password",form.data['password'])

            user = authenticate(
                request, username=form.data['email'],
                password=form.data['password']
            )
            if not user:
                form.add_error(None, "Invalid credentials")
            else:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))

    context = {'form': form}
    return render(request, template_name, context)


def register(request):

    user_form =  UserForm(request.POST or None)
    profile_form = UserProfileForm(request.POST or None)
    template_name = 'registration.html'

    user_type = request.GET.get("user_type","")
    if(user_type == "client"):
        profile_form['user_type'].initial = 1
    elif(user_type == "stylist"):
        profile_form['user_type'].initial = 2
    else:
        raise PermissionDenied()

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save(user)
            auth_login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
        
    return render(request, template_name, context)

@login_required
def salon_service(request):

    form =  ServiceForm(request.POST or None)
    template_name = 'service.html'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('service'))
    
    context = {
        'form': form,
    }
        
    return render(request, template_name, context)

@login_required(login_url="/login")
def dashboard(request):
    template_name = "dashboard.html"
    user = request.user
    
    if(user.userprofile.user_type == 1):
        appointments = Appointment.objects.filter(client = user.userprofile.id)
    elif(user.userprofile.user_type == 2):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        appointments = Appointment.objects.filter(stylist = user.userprofile.id, status=0, appointment_date__range=(today_min, today_max))
    else:
        appointments = Appointment.objects.filter(status=2)

    context = {'appointments': appointments, 'user':user}
    return render(request, template_name, context)


@login_required(login_url="/login")
def appointment_booking(request):
    template_name = "appointment_booking.html"
    client = UserProfile.objects.get(user=request.user)
    stylists = UserProfile.objects.filter(user_type=2)
    services = Service.objects.all()

    if request.method == 'POST':
        data = request.POST
        try:
            stylist = UserProfile.objects.get(id=data['stylist'])
            service = Service.objects.get(id=data['service'])
            object = {
                'service': service, 
                'status': 2, 
                'stylist':stylist, 
                'appointment_date': data['appointment_date'], 
                'gender': data['gender'],
                'client': client,
            }
            appointment = Appointment.objects.create(**object)
            if appointment:
                return HttpResponseRedirect(reverse('appointment_success'))
        except:
            print("Error while creating appointment")

    context = {'client':client, 'stylists':stylists, 'services': services}
    return render(request, template_name, context)

@login_required(login_url="/login")
def get_appointments(request):
    template_name = "admin_all_appointment_list.html"
    user = request.user
    appointments = Appointment.objects.all()
    name = request.GET.get('name','')
    if(name):
        appointments = appointments.filter(client__user__first_name__istartswith=name)
    if(user.userprofile.user_type == 2):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        appointments = appointments.filter(stylist = user.userprofile.id,status=0,appointment_date__range=(today_min, today_max))
        template_name = "stylist_appointments.html"
    context = {'user':user, 'appointments':appointments}
    return render(request, template_name, context)

@login_required(login_url="/login")
def profile(request):
    template_name = "profile.html"
    user = request.user
    context = {'user':user}
    return render(request, template_name, context)

@login_required(login_url="/login")
def get_stylists(request):
    template_name = "stylist_list.html"
    stylists = UserProfile.objects.filter(user_type=2)
    context = {'stylists':stylists}
    return render(request, template_name, context)

@login_required(login_url="/login")
def get_clients(request):
    template_name = "clients_list.html"
    appointments = Appointment.objects.all()
    context = {'appointments':appointments}
    return render(request, template_name, context)

@login_required(login_url="/login")
@csrf_exempt
def update_appointment_status(request):

    template_name = "admin_pending_appointment_list.html"
    context = {}
    status_code = 200
    if request.method == 'POST':
        data = json.loads(request.body)
        status = 0
        if(data.get('status') != 'Accepted'):
            status = 1
        try:
            appointment = Appointment.objects.get(id=data.get('id'))
            appointment.status = status
            appointment.save()
            appointments = Appointment.objects.filter(status=2)
            context = {"appointments":appointments}
        except Appointment.DoesNotExist:
            status_code = 400
            context = {"error": "Invalid Id"}
    return render(request, template_name, context, status=status_code)

@login_required(login_url="/login")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
