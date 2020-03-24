from django.conf.urls import url
from django.contrib import admin

from activity.views import (
    BucketingRoute
)

urlpatterns = [
    url(r'^bucketing/', BucketingRoute.as_view({'get': 'get_buckets', 'post': 'post'})),
]
