from django.shortcuts import render

# Create your views here.
from django.contrib.auth import (
    authenticate, login, logout,
)
from rest_framework.response import Response
from rest_framework.views import APIView


from users.models import GenericUser


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
        # TODO:: figure out how company fits in here - potentially url/subdomain
        email = request.GET.get('email')
        password = request.GET.get('password')
        first_name = request.GET.get('first_name')
        middle_name = request.GET.get('middle_name')
        last_name = request.GET.get('last_name')
        date_of_birth = request.GET.get('date_of_birth')
        gender = request.GET.get('gender')
        phone_number = request.GET.get('phone_number')

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

        # log user in here
        if user is not None:
            login(request, user)
            return Response({}, status=200)
        else:
            return Response({}, status=400)