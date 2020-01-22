from __future__ import absolute_import, division, print_function

from django.core.management.base import BaseCommand
from users.models import GenericUser


class Command(BaseCommand):
    help = 'Create a test admin user.'

    def create_bridge_admin_users(self, email, company_id='1', first_name='Bridge', last_name='Admin', gender='M', password='test1234'):
        emails = [ 'sebastiangrobelny15@gmail.com', 'jmalucchi@gmail.com', 'm.briceno09@gmail.com']
        passwords = [ 'test1234', 'test1234', 'test1234']
        company_id = 1
        for emails, passwords in zip(emails, passwords):
            admin_user = GenericUser.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                company_id=company_id,
                gender=gender
            )
            print("Your admin user is:", data['email'], ':', data['first_name'], data['last_name'])
            print("Your admin id is:", data['id'])


    def add_arguments(self, parser):
        parser.add_argument('-e', dest='email', default=None,
                            help='Email address otherwise will default to sebastiangrobelny15@gmail.com')
        parser.add_argument('-g', dest='gender', choices=['M', 'F'],
                            help='M or F, default random.')
        parser.add_argument('-p', dest='password', default='password1',
                            help="This user's password, default password1.")

    def handle(self, *args, **options):
        data = self.create_admin_user(email=options['email'], gender=options['gender'], password=options['password'])
