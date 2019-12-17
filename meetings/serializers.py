from rest_framework import serializers
from meetings.models import MeetingStructure


class MeetingActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingStructure
        fields = ('meeting_uuid','name')