from meetings.models import MeetingStructure, MeetingTemplate, MeetingComponent




def create_meeting_template_components(host, name, description, recurring, interval, public, start_date, selected_components):
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
            MeetingComponent.objects.create(
                component_id=selected_component['id'],
                meeting_template=template,
                duration=selected_component['duration'],
                agenda_item=selected_component['agenda_item']
            )
        return meeting_structure.meeting_uuid