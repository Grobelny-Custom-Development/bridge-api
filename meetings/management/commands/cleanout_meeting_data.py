from __future__ import absolute_import, division, print_function
from django.core.management.base import BaseCommand
from meetings.models import MeetingTemplate, Component, MeetingStructure


class Command(BaseCommand):
    help = ('Creates some baseline meeting templates.')
    def handle(self, *args, **options):
        print(self.cleanout_meeting_data())
    def cleanout_meeting_data(self):
        MeetingStructure.objects.all().delete()
        Component.objects.all().delete()
        MeetingTemplate.objects.all().delete()
