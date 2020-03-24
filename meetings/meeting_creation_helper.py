from meetings.models import (
    MeetingStructure, MeetingTemplate, Component, 
    BRAINSTORM, FORCED_RANK, GROUPING, BUCKETING, PRIORITIZATION
)

from activity.models import ActivityBase
from users.models import GenericUser



def create_meeting_template_components(host, name, description, recurring, interval, public, start_date, selected_components, participants):
        # Company will come here 
        company = host.company
        template = MeetingTemplate.objects.create(
            created_by = host,
            name = name,
            description = description,
            company_id = company.id,
            public = public,
            interval = interval
        )

        # TODO:: declare duration field that will sum component duration
        meeting_structure = MeetingStructure.objects.create(
            start_date = start_date,
            meeting_template = template,
            host = host,
            company_id = company.id
        )

        for selected_component in selected_components:
            component = Component.objects.create(
                meeting_template=template,
                name=selected_component['name'],
                description=selected_component['description'],
                activity_type= selected_component['activity_type'],
                duration=selected_component['duration'],
                agenda_item=selected_component['agenda_item']
            )
            ActivityBase.objects.create(meeting_structure=meeting_structure, component=component)
        for participant in participants:
            meeting_structure.participants.add(GenericUser.objects.get(id=participant['id']))

        return meeting_structure.meeting_uuid