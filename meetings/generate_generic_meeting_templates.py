from __future__ import absolute_import, division, print_function

from django.core.management.base import BaseCommand
from meetings.models import MeetingTemplate, Component, MeetingComponent
from meetings.meeting_creation_helper import create_meeting_template_components


class Command(BaseCommand):
    help = ('Creates some baseline meeting templates.')
    def handle(self, *args, **options):
        print(self.generate_generic_meeting_templates())
    def generate_generic_meeting_templates(self):
        baseline_names = ['Sprint Planning', 'Sprint Review', 'Stand Up', 'Sprint Retrospective']
        baseline_descriptions = ['Brainstorming for groups', 'Forced Ranking for groups', 'Grouping for groups', 'Bucketing for groups', 'Prioritization for groups']

        selected_compoonents = Components.objects.all()
        
        # TODO:: ensure this is working properly
        for name,description in zip(baseline_names, baseline_descriptions):
            create_meeting_template_components(host, name, description, recurring, interval, public, start_date, selected_components)
        print('Created baseline meeting templates.')