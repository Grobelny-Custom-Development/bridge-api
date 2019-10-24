from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from rest_framework.response import Response



def login_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return Response({}, status=200)
    else:

        return Response({}, status=400)