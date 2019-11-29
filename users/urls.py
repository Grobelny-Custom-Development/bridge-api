from django.conf.urls import url
from django.contrib import admin

from users.views import (
    LoginView, LogoutView, RegistrationView,
    UserRoute
)

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'token-auth/', obtain_jwt_token),
    # url(r'^login/', LoginView.as_view()),
    # url(r'^logout/', LogoutView.as_view()),
    url(r'^register/', RegistrationView.as_view()),
    url(r'^user/', UserRoute.as_view())
]
