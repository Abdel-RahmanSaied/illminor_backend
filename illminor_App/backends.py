from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework import status
from rest_framework.response import Response


class Email_Backend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try :
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )

        except User.DoesNotExist:
            return None

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try :
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
