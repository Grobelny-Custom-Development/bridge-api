from django.shortcuts import render

from django.contrib.auth import (
    authenticate, login, logout,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from meetings.models import MeetingStructure, MeetingTemplate
from meetings.serializers import MeetingActiveSerializer
import uuid



class MeetingRoute(APIView):
    permission_classes = (IsAuthenticated,) 
    # authentication_classes = (TokenAuthentication,) 
    def get(self, request):
        return Response({'message': 'hello'}, status=200)

    def post(self, request):
        # properties that will be derived from user
        host = request.user

        # Company will come here 
        company = host.company
        
        # generate UUID
        meeting_uuid = uuid.uuid4()
        template_uuid = uuid.uuid4()

        # properties that have to be filled out in Form
        name = request.data.get('name')
        description = request.data.get('description')
        public = request.data.get('public')
        recurring = request.data.get('recurring')
        interval = request.data.get('interval')
        start_date = request.data.get('start_date')

        template = MeetingTemplate.objects.create(
            created_by = host,
            name = name,
            description = description,
            company = company,
            public = public,
            interval = interval,
            template_uuid = template_uuid
        )

        # TODO:: declare duration field that will sum component duration

        MeetingStructure.objects.create(
            start_date = start_date,
            meeting_template = template,
            meeting_uuid = meeting_uuid,
            host = host,
            company = company
        )
        return Response({'message': 'bonjour'}, status=200)

class CardRoute(APIView):
    def get(self, request):
        return Response({'message': 'hello'}, status=200)

    def post(self, request):
        return Response({'message': 'bonjour'}, status=200)

class MeetingActiveRoute(APIView):
    def get(self, request):
        if request.user:
            active_meetings = MeetingStructure.objects.filter(host=request.user, end_date__isnull=True)
            return Response({'meetings': MeetingActiveSerializer(active_meetings, many=True).data}, status=200)
