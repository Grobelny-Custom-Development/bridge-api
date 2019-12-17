from django.shortcuts import render

# Create your views here.
from django.contrib.auth import (
    authenticate, login, logout,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserSerializerWithToken

from users.models import GenericUser


class LoginView(APIView):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return Response({}, status=200)
        else:

            return Response({}, status=400)


class LogoutView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({}, status=200)
        else:
            return Response({}, status=400)


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        # TODO:: figure out how company fits in here - potentially url/subdomain
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        middle_name = request.data.get('middle_name')
        last_name = request.data.get('last_name')
        date_of_birth = request.data.get('date_of_birth')
        gender = request.data.get('gender')
        phone_number = request.data.get('phone_number')
        print(request.data)
        # TODO figure out if want to log users in right away or ask to verify email
        # / other actions
        user = GenericUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number
        )
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data, status=200)
        # log user in here
        if user:
            login(request, user)
            return Response({}, status=200)
        else:
            return Response({}, status=400)


class UserRoute(APIView):
    def get(self, request):
        """
        Determine the current user by their token, and return their data
        """
        
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)