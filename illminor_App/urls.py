from django.urls import path , include
from .views import *
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', USERS_viewSets)
router.register('bloodTest', bloodTest_ViewSet)
router.register('diabtesTest', diabtesTest_ViewSet)
router.register('parkinsonTest', parkinsonTest_ViewSet)
router.register('alzhimarTest', alzhimarTest_ViewSet)
router.register('heartTest', heartTest_ViewSet)
# router.register('patient', Patient_viewSets)
urlpatterns = [
            path('login/', CustomAuthToken.as_view()),
    ]

urlpatterns = urlpatterns + router.urls


# pip install django-rest-passwordreset
