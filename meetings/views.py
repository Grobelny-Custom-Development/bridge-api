from django.shortcuts import render

from django.contrib.auth import (
    authenticate, login, logout,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import uuid


from meetings.models import MeetingStructure, MeetingTemplate, MeetingComponent, Component
from meetings.serializers import MeetingActiveSerializer, ComponentSerializer, MeetingActiveComponentsSerializer, MeetingTemplateSerializer

import ast



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
        name = request.POST.get('name')
        description = request.POST.get('description')
        public = request.POST.get('public')
        recurring = request.POST.get('recurring')
        interval = request.POST.get('interval')
        start_date = request.POST.get('start_date')
        selected_components = ast.literal_eval(request.POST.get('selected_components'))
        print(selected_components)

        template = MeetingTemplate.objects.create(
            created_by = host,
            name = name,
            description = 'Hello',
            company_id = company.id,
            public = True,
            interval = interval,
            template_uuid = template_uuid
        )

        # TODO:: declare duration field that will sum component duration

        meeting_structure = MeetingStructure.objects.create(
            start_date = start_date,
            meeting_template = template,
            meeting_uuid = meeting_uuid,
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
            
        return Response({'meeting_uuid':meeting_structure.meeting_uuid }, status=200)

class CardRoute(APIView):
    def get(self, request):
        return Response({'message': 'hello'}, status=200)

    def post(self, request):
        return Response({'message': 'bonjour'}, status=200)

class MeetingActiveRoute(viewsets.ViewSet):
    def get_active_list(self, request):
        if request.user:
            active_meetings = MeetingStructure.objects.filter(host=request.user, end_date__isnull=True)
            print(active_meetings)
            return Response({'meetings': MeetingActiveSerializer(active_meetings, many=True).data}, status=200)

    def get_active_single(self, request):
        if request.user:
            meeting_uuid = request.GET.get('meeting_uuid')
            active_meeting = MeetingStructure.objects.get(meeting_uuid=meeting_uuid)
            return Response({'meeting': MeetingActiveComponentsSerializer(active_meeting).data}, status=200)

class ComponentRoute(APIView):
    def get(self, request):
        if request.user:
            components = Component.objects.all()
            return Response({'components': ComponentSerializer(components, many=True).data}, status=200)

class TemplateActiveRoute(APIView):
    def get(self, request):
        if request.user:
            meeting_templates = MeetingTemplate.objects.all()
            return Response({'templates': MeetingTemplateSerializer(meeting_templates, many=True).data}, status=200)