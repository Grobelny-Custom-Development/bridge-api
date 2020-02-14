from __future__ import absolute_import, division, print_function
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from meetings.models import Component, ACTIVITY_CHOICES


class Command(BaseCommand):
    help = ('Creates some baseline meeting components.')
    def handle(self, *args, **options):
        print(self.generate_generic_meeting_components())
    
    def generate_generic_meeting_components(self):
        baseline_names = ['Brainstorm', 'Forced Rank', 'Grouping', 'Bucketing', 'Prioritization']
        baseline_descriptions = ['Brainstorming for groups', 'Forced Ranking for groups', 'Grouping for groups', 'Bucketing for groups', 'Prioritization for groups']

        # TODO:: ensure this is working properly
        # content_type
        # object_id
        for name, description, activity_choice in zip(baseline_names, baseline_descriptions, ACTIVITY_CHOICES):
            Component.objects.create(
                name=name,
                description=description,
                acitvity_type =activity_choice,
                duration = timedelta(minutes=10),
                agenda_item=name
            )
        print('Created baseline components.')
        