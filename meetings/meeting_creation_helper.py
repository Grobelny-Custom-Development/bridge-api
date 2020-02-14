from meetings.models import (
    MeetingStructure, MeetingTemplate, Component, 
    BRAINSTORM, FORCED_RANK, GROUPING, BUCKETING, PRIORITIZATION
)

from activity.models import (
    BrainstormActivity, ForcedRankActivity, GroupingActivity, BucketingActivity,
    PrioritizationActivity
)




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
            component = Component.objects.create(
                meeting_template=template,
                name=selected_component['name'],
                description=selected_component['description'],
                acitvity_type= selected_component['activity_type'],
                duration=selected_component['duration'],
                agenda_item=selected_component['agenda_item']
            )
            if selected_component['activity_type'] == BRAINSTORM:
                BrainstormActivity.objects.create(meeting_structure=meeting_structure, component=component)
            elif selected_component['activity_type'] == FORCED_RANK:
                ForcedRankActivity.objects.create(meeting_structure=meeting_structure, component=component)

            elif selected_component['activity_type'] == GROUPING:
                GroupingActivity.objects.create(meeting_structure=meeting_structure, component=component)
            
            elif selected_component['activity_type'] == BUCKETING:
                BucketingActivity.objects.create(meeting_structure=meeting_structure, component=component)
            
            elif selected_component['activity_type'] == PRIORITIZATION:
                PrioritizationActivity.objects.create(meeting_structure=meeting_structure, component=component)

        return meeting_structure.meeting_uuid