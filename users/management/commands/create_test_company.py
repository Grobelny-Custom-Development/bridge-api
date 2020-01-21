
from __future__ import absolute_import, division, print_function

from django.core.management.base import BaseCommand
from bridge.time_helper import TimeHelper
from users.models import Company


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(self.create_test_company())

    def create_test_company(self):
        company = Company.objects.create(
            name='Bridge Test Inc. 2020',
            effective_start=TimeHelper.get_utc_now_datetime()
        )
        print('Company created the id is:{}'.format(company.id))