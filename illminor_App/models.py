from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import date
from dateutil.relativedelta import relativedelta
import os
from django.urls import reverse
# Create your models here.

gander_choices = [
    ("Male", "Male"),
    ("Female", "Female")
]

class DOCTORS(models.Model) :
    user = models.OneToOneField(User,  primary_key= True,unique=True, on_delete=models.CASCADE , default= None)
    name = models.CharField(max_length=255, null= False)
    profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg', null=False)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=14, null=False)
    gander = models.CharField(max_length=6, choices=gander_choices, null=False, default="Male")
    age = models.IntegerField(null=False)
    def __str__(self):
        return self.name

class PATIENTS(models.Model) :
    user = models.OneToOneField(User,  primary_key= True,unique=True, on_delete=models.CASCADE , default= None)
    name = models.CharField(max_length=255, null= False)
    profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg', null=False)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=14, null=False)
    gander = models.CharField(max_length=6, choices=gander_choices, null=False, default="Male")
    age = models.IntegerField(null=False)
    def __str__(self):
        return self.name



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)