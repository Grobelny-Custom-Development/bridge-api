from django.conf.urls import url
from django.contrib import admin

from meetings.views import (
    MeetingRoute, CardRoute,
    MeetingActiveRoute,
)

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^structure/create/', MeetingRoute.as_view()),
    url(r'^card/create/', CardRoute.as_view()),
    url(r'^active/', MeetingActiveRoute.as_view())
]
