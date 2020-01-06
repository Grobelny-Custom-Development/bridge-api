from rest_framework import serializers
from meetings.models import MeetingStructure, Component


class MeetingActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid','name')

class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = ('name', 'description')