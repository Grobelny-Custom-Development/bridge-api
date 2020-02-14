from __future__ import absolute_import, division, print_function
from datetime import timedelta
from django.core.management.base import BaseCommand
from bridge.time_helper import TimeHelper
from meetings.models import MeetingTemplate, Component, ACTIVITY_CHOICES
from meetings.meeting_creation_helper import create_meeting_template_components
from users.models import GenericUser


class Command(BaseCommand):
    help = ('Creates some baseline meeting templates.')
    def handle(self, *args, **options):
        print(self.generate_generic_meeting_templates())
    def generate_generic_meeting_templates(self):
        baseline_names = ['Sprint Planning', 'Sprint Review', 'Stand Up', 'Sprint Retrospective']
        baseline_descriptions = ['Sprint Planning for groups', 'Forced Ranking for groups', 'Grouping for groups', 'Bucketing for groups', 'Prioritization for groups']
        baseline_component_names = ['Brainstorm', 'Forced Rank', 'Grouping', 'Bucketing', 'Prioritization']
        baseline_component_descriptions = ['Brainstorming for groups', 'Forced Ranking for groups', 'Grouping for groups', 'Bucketing for groups', 'Prioritization for groups']
        hosts = GenericUser.objects.all()
        for host in hosts:
            selected_components = []
            for name, description, activity_choice in zip(baseline_component_names, baseline_component_descriptions, ACTIVITY_CHOICES):
                selected_component = {
                    'name' : name,
                    'description' : description,
                    'activity_type' : activity_choice[0],
                    'duration' : timedelta(minutes=10),
                    'agenda_item' : name
                }
                selected_components.append(selected_component)
            start_date = TimeHelper.get_utc_now_datetime()
            recurring = True
            interval = 'Week'
            public = True
            
            # TODO:: ensure this is working properly
            for name,description in zip(baseline_names, baseline_descriptions):
                create_meeting_template_components(host, name, description, recurring, interval, public, start_date, selected_components)
        print('Created baseline meeting templates.')