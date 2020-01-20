from django.shortcuts import render

from django.contrib.auth import (
    authenticate, login, logout,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import uuid
import ast

from meetings.models import MeetingStructure, MeetingTemplate, MeetingComponent, Component
from meetings.serializers import MeetingActiveSerializer, ComponentSerializer, MeetingActiveComponentsSerializer, MeetingTemplateSerializer

from meetings.meeting_creation_helper import create_meeting_template_components



class MeetingRoute(APIView):
    permission_classes = (IsAuthenticated,) 
    # authentication_classes = (TokenAuthentication,) 
    def get(self, request):
        return Response({'message': 'hello'}, status=200)

    def post(self, request):
        # properties that will be derived from user
        host = request.user

        # properties that have to be filled out in Form
        name = request.POST.get('name')
        description = request.POST.get('description')
        public = request.POST.get('public') == "true"
        recurring = request.POST.get('recurring') == "true"
        interval = request.POST.get('interval')
        start_date = request.POST.get('start_date')
        selected_components = ast.literal_eval(request.POST.get('selected_components'))

        meeting_uuid = create_meeting_template_components(host, name, description, recurring, interval, public, start_date, selected_components)
            
        return Response({'meeting_uuid': meeting_uuid }, status=200)

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
            meeting_templates = MeetingTemplate.objects.filter(public=True)
            return Response({'templates': MeetingTemplateSerializer(meeting_templates, many=True).data}, status=200)