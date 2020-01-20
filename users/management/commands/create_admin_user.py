from __future__ import absolute_import, division, print_function

from django.core.management.base import BaseCommand
from users.models import GenericUser


class Command(BaseCommand):
    help = 'Create a test admin user.'

    def create_admin_user(self, email, company_id='1', first_name='Bridge', last_name='Admin', gender='M', password='test1234'):
        admin_user = GenericUser.objects.create_superuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            gender=gender
        )
        return admin_user.__dict__


    def add_arguments(self, parser):
        parser.add_argument('-e', dest='email', default=None,
                            help='Email address otherwise will default to sebastiangrobelny15@gmail.com')
        parser.add_argument('-g', dest='gender', choices=['M', 'F'],
                            help='M or F, default random.')
        parser.add_argument('-p', dest='password', default='password1',
                            help="This user's password, default password1.")

    def handle(self, *args, **options):
        data = self.create_admin_user(email=options['email'], gender=options['gender'], password=options['password'])
        print("Your admin user is:", data['email'], ':', data['first_name'], data['last_name'])
        print("Your admin id is:", data['id'])