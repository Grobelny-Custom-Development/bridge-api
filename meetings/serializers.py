from rest_framework import serializers
from meetings.models import MeetingStructure, Component, MeetingTemplate

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
    components = serializers.SerializerMethodField()
    class Meta:
        model = MeetingTemplate
        fields = ('name', 'description', 'components')
    
    def get_components(self, meeting_template):
        components = Component.objects.filter(meeting_template=meeting_template)
        return ComponentSerializer(components, many=True).data
class MeetingActiveComponentsSerializer(serializers.ModelSerializer):
    meeting_template = MeetingTemplateComponentSerializer(required=False)
    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid', 'start_date', 'meeting_template')

class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = ('name', 'description', 'agenda_item', 'duration', 'id')