from django.shortcuts import render

# Create your views here.
from django.contrib.auth import (
    authenticate, login, logout,
)
from rest_framework.response import Response
from rest_framework.views import APIView



class LoginView(APIView):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

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

    def post(self, request):


        return Response({}, status=200)