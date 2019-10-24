from django.conf.urls import url
from django.contrib import admin

from users.views import login_user

urlpatterns = [
    url(r'^login/', login_user),
]
