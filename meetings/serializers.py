from rest_framework import serializers
from meetings.models import MeetingStructure, Component, MeetingTemplate
from activity.models import ActivityBase

class MeetingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTemplate
        fields = ('name', 'description')
class MeetingActiveSerializer(serializers.ModelSerializer):
    meeting_template = MeetingTemplateSerializer(required=False)
    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid', 'start_date', 'meeting_template')

class MeetingTemplateComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTemplate
        fields = ('name', 'description')


class ActivitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    agenda_item = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    activity_type = serializers.SerializerMethodField()
    class Meta:
        model = ActivityBase
        fields = ('name', 'description', 'agenda_item', 'duration', 'activity_uuid',
                   'activity_type')
    
    def get_name(self, activity):
        return activity.component.name
    
    def get_description(self, activity):
        return activity.component.description

    def get_agenda_item(self, activity):
        return activity.component.agenda_item
    
    def get_activity_type(self, activity):
        return activity.component.activity_type
    
    def get_duration(self, activity):
        return activity.component.duration
                
class MeetingActiveComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid', 'start_date')

class ComponentSerializer(serializers.ModelSerializer):
    activity_uuid = serializers.SerializerMethodField()
    class Meta:
        model = Component
        fields = ('name', 'description', 'agenda_item', 'duration', 'activity_uuid',
                   'activity_type', 'activity_uuid')
        read_only_fields = ('name', 'description', 'agenda_item', 'duration', 'activity_uuid','acitvity_type', 'activity_uuid')
    
    def get_activity_uuid(self, component):
        meeting_structure = self.context.get('meeting_structure')
        activity = ActivityBase.objects.get(component=component, meeting_structure=meeting_structure)
        return activity.activity_uuid
