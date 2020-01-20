from __future__ import absolute_import, division, print_function

from django.core.management.base import BaseCommand
from meetings.models import Component


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
        for name,description in zip(baseline_names, baseline_descriptions):
            Component.objects.create(
                name=name,
                description=description,
                object_id=1
            )
        print('Created baseline components.')
        