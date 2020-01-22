from __future__ import absolute_import, division, print_function
from datetime import timedelta
from django.core.management.base import BaseCommand
from bridge.time_helper import TimeHelper
from meetings.models import MeetingTemplate, Component, MeetingComponent
from meetings.meeting_creation_helper import create_meeting_template_components
from users.models import GenericUser


class Command(BaseCommand):
    help = ('Creates some baseline meeting templates.')
    def handle(self, *args, **options):
        print(self.generate_generic_meeting_templates())
    def generate_generic_meeting_templates(self):
        baseline_names = ['Sprint Planning', 'Sprint Review', 'Stand Up', 'Sprint Retrospective']
        baseline_descriptions = ['Sprint Planning for groups', 'Forced Ranking for groups', 'Grouping for groups', 'Bucketing for groups', 'Prioritization for groups']
        hosts = GenericUser.objects.all()
        selected_components = list(Component.objects.values())
        print(selected_components)
        for host in hosts:
            for count, selected_component in enumerate(selected_components):
                
                selected_component['agenda_item'] = 'Agenda Item {}'.format(count)
                selected_component['duration'] = timedelta(minutes=count)

                # replace
                selected_components[count] = selected_component

            start_date = TimeHelper.get_utc_now_datetime()
            recurring = True
            interval = 'Week'
            public = True
            
            # TODO:: ensure this is working properly
            for name,description in zip(baseline_names, baseline_descriptions):
                create_meeting_template_components(host, name, description, recurring, interval, public, start_date, selected_components)
        print('Created baseline meeting templates.')