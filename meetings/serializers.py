from rest_framework import serializers
from meetings.models import MeetingStructure, MeetingComponent, Component, MeetingTemplate, Cards

class MeetingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTemplate
        fields = ('name', 'description')
class MeetingActiveSerializer(serializers.ModelSerializer):
    meeting_template = MeetingTemplateSerializer(required=False)
    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid', 'start_date', 'meeting_template')

class MeetingComponentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='component.name')
    class Meta:
        model = MeetingComponent
        fields = ('agenda_item', 'duration', 'name')

class MeetingTemplateComponentSerializer(serializers.ModelSerializer):
    components = MeetingComponentSerializer(required=False, many=True, source='meetingcomponent_set')
    class Meta:
        model = MeetingTemplate
        fields = ('name', 'description', 'components')

class MeetingActiveComponentsSerializer(serializers.ModelSerializer):
    meeting_template = MeetingTemplateComponentSerializer(required=False)
    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid', 'start_date', 'meeting_template')

class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = ('name', 'description', 'id')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ('content',)