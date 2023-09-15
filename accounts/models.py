# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import RegexValidator


class DateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

GENDER_CHOICE_MALE = 'male'
GENDER_CHOICE_FEMALE = 'female'
GENDER_CHOICE_OTHER = 'other'

GENDER_CHOICES = (
    (GENDER_CHOICE_MALE, 'Male'),
    (GENDER_CHOICE_FEMALE, 'Female'),
    (GENDER_CHOICE_OTHER, 'Other'),
)

USERTYPE_CHOICE_ADMIN = 'Admin'
USERTYPE_CHOICE_CLIENT = 'Client'
USERTYPE_CHOICE_STYLIST = 'Stylist'
USERTYPE_CHOICES = (
    (0, USERTYPE_CHOICE_ADMIN,),
    (1, USERTYPE_CHOICE_CLIENT),
    (2, USERTYPE_CHOICE_STYLIST),
)

class UserProfile(DateTimeBase):
    
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=100,choices=GENDER_CHOICES, null=True, blank=True)
    
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    user_type = models.IntegerField(choices=USERTYPE_CHOICES, default=1, null=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return u"%s" % self.user.email


class Service(DateTimeBase):
    name = models.CharField(max_length=320)
    description = models.TextField()

    def __str__(self):
        return u"%s" % self.name


class Appointment(DateTimeBase):

    APPOINTMENT_STATUS_CHOICE_ACCEPTED = 'Accepted'
    APPOINTMENT_STATUS_CHOICE_DECLINED = 'Declined'
    APPOINTMENT_STATUS_CHOICE_PENDING = 'Pending'
    APPOINTMENT_STATUS_CHOICES = (
        (0, APPOINTMENT_STATUS_CHOICE_ACCEPTED),
        (1, APPOINTMENT_STATUS_CHOICE_DECLINED),
        (2, APPOINTMENT_STATUS_CHOICE_PENDING),
    )

    client = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,null=True, related_name='client')
    stylist = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,null=True, related_name='stylist')
    gender = models.CharField(max_length=100,choices=GENDER_CHOICES)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True)
    appointment_date = models.DateTimeField()
    status = models.IntegerField(choices=APPOINTMENT_STATUS_CHOICES, default=2, null=True)

    def __str__(self):
        return u"%s-%s" %(self.client.user.first_name, self.stylist.user.first_name)



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()