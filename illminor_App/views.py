from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, mixins, viewsets
from rest_framework import status, filters

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .permissons import PatientPermission
# from django.db.models import Q
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser
# Create your views here.

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            is_doctor = DOCTORS.objects.filter(user_id=user.pk).exists()

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'is_doctor': is_doctor
            })
        else:
            return Response({"Response":"username or password was incorrect"} , status=status.HTTP_401_UNAUTHORIZED)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Doctors_viewSets(viewsets.ModelViewSet):
    permission_classes = [PatientPermission,]
    queryset = DOCTORS.objects.all()
    serializer_class = DoctorSerializer
    # http_method_names = ['post']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'name', 'user__email', 'phone_number', ]
    filterset_fields = ['user__id','user__username', 'name', 'user__email', 'phone_number', ]
    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        name = request.data["name"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        email = request.data["email"]
        profile_picture = request.data["profile_picture"]
        bio = request.data["bio"]
        phone_number = request.data["phone_number"]
        gander = request.data["gander"]
        age = request.data["age"]
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        serializer = ClientSerializer(data=request.data)
        if User.objects.filter(username=username).exists():
            return Response({"Response": "username already exist !"}, status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=email).exists():
            return Response({"Response": "email already exist !"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if serializer.is_valid() and password1 == password2:
                user = User.objects.create_user(username=username, password=password1, email=email , first_name=first_name , last_name=last_name)
                nuser = DOCTORS.objects.create(user=user, name=name, profile_picture=profile_picture,
                                               bio=bio
                                               , phone_number=phone_number, gander=gander, age=age,
                                               )
                token = Token.objects.get(user=user).key
                nuser.save()
                user.save()
                return Response({"token": token}, status=status.HTTP_201_CREATED)
            else:
                # return Response({"Response": 'password must match.'}, status.HTTP_401_UNAUTHORIZED)
                return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
