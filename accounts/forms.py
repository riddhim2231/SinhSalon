from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from .models import *

import re

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password', 'confirm_password')
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "password and confirm password do not match.")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.username = self.cleaned_data['email']
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField()
    address = forms.Textarea()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    user_type = forms.ChoiceField(choices=USERTYPE_CHOICES)
    age = forms.IntegerField()


    class Meta:
        model = UserProfile
        fields = ("phone_number", "address","gender", "age","user_type")

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        phone_number = cleaned_data['phone_number']
        regex=re.compile('^(\+\d{1,3})?,?\s?\d{8,13}')
        if(not regex.match(phone_number)):
            self.add_error("phone_number", "Invalid phone number")

    def save(self, user, commit=True):
        instance = super(UserProfileForm, self).save(commit=False)

        if commit:
            instance.user = user
            instance.save()
        return instance


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('gender', 'appointment_date', 'stylist', 'service',)

    def save(self, user, commit=True):
        instance = super(AppointmentForm, self).save(commit=False)

        if commit:
            instance.client = user
            instance.save()
        return instance

class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ('name', 'description',)


        

