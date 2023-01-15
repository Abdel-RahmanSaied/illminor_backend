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

from .permissons import *
# from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser


# Create your views here.

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            try :
                doctor = USERS.objects.get(user_id=user.pk).is_doctor
            except :
                doctor = False

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'user_name': user.username,
                'email': user.email,
                'is_doctor': doctor
            })
        else:
            return Response({"Response":"username or password was incorrect"} , status=status.HTTP_401_UNAUTHORIZED)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class USERS_viewSets(viewsets.ModelViewSet):
    permission_classes = [UserPermission,]
    queryset = USERS.objects.all()
    serializer_class = USERSSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'name', 'user__email', 'phone_number', ]
    filterset_fields = ['user__id','user__username', 'name', 'user__email', 'phone_number', ]

    def create(self, request, *args, **kwargs):
        # data_1 = {key: value for key, value in request.data.items() if key in USERSSS.Meta.fields}
        data_1 = {
            'username': request.data["username"],
            'first_name': request.data["first_name"],
            'last_name': request.data["last_name"],
            'email': request.data["email"],
            'password1': request.data["password1"],
            'password2': request.data["password2"],
        }
        try :
            is_doctor = request.data["is_doctor"]
        except Exception as e :
            is_doctor = False
            print(e)
        data_2 = {
            'name': request.data["name"],
            'profile_picture': request.data["profile_picture"],
            'bio': request.data["bio"],
            'phone_number': request.data["phone_number"],
            'gander': request.data["gander"],
            'age': request.data["age"],
            'is_doctor':is_doctor
        }
        serializer= USERSSerializer(data=data_2,  context={'request': request})
        if User.objects.filter(username=data_1['username']).exists():
            return Response({"Response": "username already exist !"}, status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=data_1['email']).exists():
            return Response({"Response": "email already exist !"}, status=status.HTTP_401_UNAUTHORIZED)
        elif data_1['password1'] != data_1['password2']:
            return Response({"Response": "Passwords not matched !"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if serializer.is_valid():
                user = User.objects.create_user(username=data_1["username"],
                                                password=data_1["password1"], email=data_1["email"],
                                                first_name=data_1["first_name"],
                                                last_name=data_1["last_name"])

                serializer.save(user=user)
                user.save()
                # instance = (instance_1, instance_2)

                token = Token.objects.get(user=user).key
                return Response({"token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class bloodTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = bloodTest.objects.all()
    serializer_class = bloodTestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['user__id','user__username', 'id', 'date', "result"]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            result = serializer.predict()
            serializer.save(result=result)
            return Response({"response": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class diabtesTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = diabtesTest.objects.all()
    serializer_class = diabtesTestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['user__id','user__username', 'id', 'date', "result"]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.predict()
            serializer.save(result=result)
            return Response({"response": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)



class parkinsonTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = parkinsonTest.objects.all()
    serializer_class = parkinsonTestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['user__id','user__username', 'id', 'date', "result"]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            result = serializer.predict()
            serializer.save(result=result)
            return Response({"response": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)



class alzhimarTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = alzhimarTest.objects.all()
    serializer_class = alzhimarTestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['user__id','user__username', 'id', 'date', "result"]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            result = serializer.predict()
            serializer.save(result=result)
            return Response({"response": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class heartTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = heartTest.objects.all()
    serializer_class = heartTestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['user__id','user__username', 'id', 'date', "result"]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            result = serializer.predict()
            serializer.save(result=result)
            return Response({"response": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

