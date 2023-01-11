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


class USERS(models.Model) :
    user = models.OneToOneField(User,  primary_key= True,unique=True, on_delete=models.CASCADE )
    name = models.CharField(max_length=255, null= False)
    profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg', null=False)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=14, null=False)
    gander = models.CharField(max_length=6, choices=gander_choices, null=False, default="Male")
    age = models.IntegerField(null=False)
    is_doctor = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class bloodTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True ,auto_created=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    bmi = models.FloatField()
    glucouse = models.FloatField()
    insuline = models.FloatField()
    homa = models.FloatField()
    leptin = models.FloatField()
    adiponcetin = models.FloatField()
    resistiin = models.FloatField()
    mcp = models.FloatField()
    date = models.DateField(default=date.today , null=False)
    result = models.CharField(max_length=20 , null=True)
    def __str__(self):
        return self.date

class diabtesTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pregnancies = models.FloatField()
    glucose = models.FloatField()
    bloodpressure = models.FloatField()
    skinthickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    dpf = models.FloatField()
    age = models.IntegerField()
    result = models.CharField(max_length=20)

    def __str__(self):
        return self.date

class parkinsonTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MDVP_Fo_Hz = models.FloatField()
    MDVP_Fhi_Hz = models.FloatField()
    MDVP_Flo_Hz = models.FloatField()
    MDVP_Jitter = models.FloatField()
    MDVP_Jitter_Abs = models.FloatField()
    MDVP_RAP = models.FloatField()
    MDVP_PPQ = models.FloatField()
    Jitter_DDP = models.FloatField()
    MDVP_Shimmer = models.FloatField()
    MDVP_Shimmer_dB = models.FloatField()
    Shimmer_APQ3 = models.FloatField()
    Shimmer_APQ5 = models.FloatField()
    MDVP_APQ = models.FloatField()
    Shimmer_DDA = models.FloatField()
    NHR = models.FloatField()
    HNR = models.FloatField()
    RPDE = models.FloatField()
    DFA = models.FloatField()
    spread1 = models.FloatField()
    spread2 = models.FloatField()
    D2 = models.FloatField()
    PPE = models.FloatField()
    result = models.CharField(max_length=20)

    def __str__(self):
        return self.date

class alzhimarTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=15, choices=gander_choices)
    Age = models.FloatField()
    EDUC = models.FloatField()
    SES = models.FloatField()
    MMSE = models.FloatField()
    eTIV = models.FloatField()
    nWBV = models.FloatField()
    ASF = models.FloatField()
    result = models.CharField(max_length=20)
    def __str__(self):
        return self.date
class heartTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    age = models.FloatField()
    sex = models.CharField(max_length=15, choices=gander_choices)
    cp = models.FloatField()
    trestbps = models.FloatField()
    chol = models.FloatField()
    fbs = models.FloatField()
    restecg = models.FloatField()
    thalach = models.FloatField()
    exang = models.FloatField()
    oldpeak = models.FloatField()
    slope = models.FloatField()
    ca = models.FloatField()
    thal = models.FloatField()
    result = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.date


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)