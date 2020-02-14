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

from meetings.models import ( 
    MeetingStructure, MeetingTemplate, Component, 
    BRAINSTORM, FORCED_RANK, GROUPING, BUCKETING, PRIORITIZATION
)

from activity.models import (
    Cards, PrioritizationActivity, BrainstormActivity,
    PrioritizedCards, BrainstormCards
)
from meetings.serializers import (
    MeetingActiveSerializer, ComponentSerializer, 
    MeetingActiveComponentsSerializer, MeetingTemplateSerializer
)

from activity.serializers import (
    CardSerializer
)

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

class CardRoute(viewsets.ViewSet):
    def get_user_cards(self, request):
        meeting_uuid = request.GET.get('meeting_uuid')
        # TODO:: figure out how to reference meetings on these
        meeting = MeetingStructure.objects.get(meeting_uuid=meeting_uuid)
        brainstorm_activity = BrainstormActivity.objects.filter(meeting_structure=meeting).first()
        if brainstorm_activity:
            brainstorm_cards = BrainstormCards.objects.filter(brainstorm_activity=brainstorm_activity, created_by=request.user).values_list('card_id', flat=True)
            current_cards = Cards.objects.filter(meeting__meeting_uuid=meeting_uuid, id__in=brainstorm_cards)
            return Response({'cards': CardSerializer(current_cards, many=True).data, 'brainstorm_activity_id': brainstorm_activity.id}, status=200)
        else:
            return Response(status=400)

    def get_active_cards(self, request):
        meeting_uuid = request.GET.get('meeting_uuid')
        current_cards = Cards.objects.filter(meeting__meeting_uuid=meeting_uuid, active=True)
        return Response({'cards': CardSerializer(current_cards, many=True).data}, status=200)

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

class BrainstormRoute(viewsets.ViewSet):
    def post(self, request):
        meeting_uuid = request.POST.get('meeting_uuid')
        content = request.POST.get('content')

        meeting = MeetingStructure.objects.get(meeting_uuid=meeting_uuid)
        brainstorm_activity = BrainstormActivity.objects.filter(meeting_structure=meeting).first()
        if brainstorm_activity:
            card = Cards.objects.create(
                content=content,
                meeting=meeting
            )
            BrainstormCards.objects.create(
                card=card,
                brainstorm_activity=brainstorm_activity,
                created_by=request.user
            )
            brainstorm_cards = BrainstormCards.objects.filter(brainstorm_activity=brainstorm_activity, created_by=request.user).values_list('card_id', flat=True)
            current_cards = Cards.objects.filter(meeting__meeting_uuid=meeting_uuid, id__in=brainstorm_cards)
            return Response({'brainstorm_cards': CardSerializer(current_cards, many=True).data}, status=200)


class PrioritizationRoute(viewsets.ViewSet):
    def get(self, request):
        meeting_uuid = request.GET.get('meeting_uuid')
        current_cards = Cards.objects.filter(meeting__meeting_uuid=meeting_uuid, active=True)
        return Response({'brainstorm_cards': CardSerializer(current_cards, many=True).data}, status=200)
    
    def post(self, request):
        meeting_uuid = request.data.get('meeting_uuid')
        meeting = MeetingStructure.objects.get(meeting_uuid=meeting_uuid)
        prioritization_activity = PrioritizationActivity.objects.get(meeting_structure=meeting)
        if prioritization_activity:
            prioritized_cards = request.data.get('prioritized_cards')

            # backend assumes front-end sends in order that cards should be ranked
            for rank, prioritized_card in enumerate(prioritized_cards):
                PrioritizedCards.objects.create(
                    card_id=prioritized_card['id'],
                    prioritization_activity = prioritization_activity,
                    ranked_by = request.user,
                    rank = rank
                )
            return Response('Success', status=200)

class ForcedRankRoute(viewsets.ViewSet):
    def get(self, request):
        meeting_uuid = request.GET.get('meeting_uuid')
        # all active cards
        current_cards = Cards.objects.filter(meeting__meeting_uuid=meeting_uuid)
        return Response({'cards': CardSerializer(current_cards, many=True).data}, status=200)
    
    def post(self, request):
        meeting_uuid = request.data.get('meeting_uuid')
        meeting = MeetingStructure.objects.get(meeting_uuid=meeting_uuid)
        prioritization_activity = PrioritizationActivity.objects.get(meeting_structure=meeting)
        if prioritization_activity:
            prioritized_cards = request.data.get('prioritized_cards')

            # backend assumes front-end sends in order that cards should be ranked
            for rank, prioritized_card in enumerate(prioritized_cards):
                PrioritizedCards.objects.create(
                    card_id=prioritized_card['id'],
                    prioritization_activity = prioritization_activity,
                    ranked_by = request.user,
                    rank = rank
                )
            return Response('Success', status=200)