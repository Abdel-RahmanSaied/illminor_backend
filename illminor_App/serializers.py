from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta :
        model = DOCTORS
        fields = "__all__"
    def get_user(self, instance):
        return instance.user.username
    def get_user_id(self, instance):
        return instance.user.id