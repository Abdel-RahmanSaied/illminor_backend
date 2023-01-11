from django.urls import path , include
from .views import *
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('doctor', Doctors_viewSets)
# router.register('patient', Patient_viewSets)
urlpatterns = [
            path('login/', CustomAuthToken.as_view()),
    ]

urlpatterns = urlpatterns + router.urls


# pip install django-rest-passwordreset
