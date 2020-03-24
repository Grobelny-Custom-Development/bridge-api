from __future__ import absolute_import, division, print_function
from django.core.management.base import BaseCommand
from activity.models import Buckets, ActivityBase
from users.models import GenericUser


class Command(BaseCommand):
    help = ('Creates default Bucketing Activity Buckets.')

    def handle(self, *args, **options):
        print(self.generate_default_buckets())

    def generate_default_buckets(self):
        default_user = GenericUser.objects.first()
        bucketing_names = ['Bucket1', 'Bucket2', 'Bucket3', 'Bucket4']
        bucketing_activities = ActivityBase.objects.filter(
            component__activity_type='bucketing').values_list(
            'id', flat=True)
        for bucketing_activity, bucketing_name in zip(
                bucketing_activities, bucketing_names):
            Buckets.objects.create(
                bucketing_activity_id=bucketing_activity,
                name=bucketing_name,
                created_by=default_user
            )
        print('Creates default Bucketing Activity Buckets.')
