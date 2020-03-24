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
    BRAINSTORM, FORCED_RANK, GROUPING, BUCKETING, PRIORITIZATION,
    ACTIVITY_CHOICES
)

from activity.models import (
    Cards, ActivityBase,
    PrioritizedCards
)
from users.serializers import UserSerializer
from meetings.serializers import (
    MeetingActiveSerializer, ComponentSerializer,
    MeetingActiveComponentsSerializer,
    ActivitySerializer,
    MeetingTemplateSerializer
)

from activity.serializers import (
    CardSerializer
)

from meetings.meeting_creation_helper import create_meeting_template_components


# TODO:: consolidate card calls
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
        selected_components = ast.literal_eval(
            request.POST.get('selected_components'))

        meeting_uuid = create_meeting_template_components(
            host,
            name,
            description,
            recurring,
            interval,
            public,
            start_date,
            selected_components)

        return Response({'meeting_uuid': meeting_uuid}, status=200)


class CardRoute(viewsets.ViewSet):
    def get_user_cards(self, request):
        activity_uuid = request.GET.get('activity_uuid')
        activity = ActivityBase.objects.get(activity_uuid=activity_uuid)
        if activity:
            current_cards = Cards.objects.filter(
                activity_created_by=activity, user_created=request.user)
            return Response({'cards': CardSerializer(
                current_cards, many=True).data, 'brainstorm_activity_id': activity.id}, status=200)
        else:
            return Response(status=400)

    def get_active_cards(self, request):
        activity_uuid = request.GET.get('activity_uuid')

        # TODO:: change this when changing how data gets input into activities
        activity = ActivityBase.objects.get(activity_uuid=activity_uuid)
        current_cards = Cards.objects.filter(
            activity_created_by=activity.data_input, active=True)
        return Response({'cards': CardSerializer(
            current_cards, many=True).data}, status=200)

    def post(self, request):
        return Response({'message': 'bonjour'}, status=200)


class MeetingActiveRoute(viewsets.ViewSet):
    def get_active_list(self, request):
        if request.user:
            active_meetings = MeetingStructure.objects.filter(
                host=request.user, end_date__isnull=True)
            return Response({'meetings': MeetingActiveSerializer(
                active_meetings, many=True).data}, status=200)

    def get_active_single(self, request):
        if request.user:
            meeting_uuid = request.GET.get('meeting_uuid')
            active_meeting = MeetingStructure.objects.get(
                meeting_uuid=meeting_uuid)
            components = Component.objects.filter(
                meeting_template=active_meeting.meeting_template)
            participants = active_meeting.participants
            response_data = {
                'meeting': MeetingActiveSerializer(active_meeting).data,
                'activities': ComponentSerializer(
                    components,
                    context={
                        'meeting_structure': active_meeting},
                    many=True).data,
                'participants': UserSerializer(
                    participants,
                    many=True).data}
            return Response(response_data, status=200)


class ComponentRoute(APIView):
    def get(self, request):
        if request.user:
            components = []
            for count, component in enumerate(ACTIVITY_CHOICES):
                components.append(
                    {'id': count, 'name': component[1], 'activity_type': component[0]})
            return Response({'components': components}, status=200)


class TemplateActiveRoute(APIView):
    def get(self, request):
        if request.user:
            meeting_templates = MeetingTemplate.objects.filter(public=True)
            return Response({'templates': MeetingTemplateSerializer(
                meeting_templates, many=True).data}, status=200)


class BrainstormRoute(viewsets.ViewSet):
    def post(self, request):
        activity_uuid = request.POST.get('activity_uuid')
        content = request.POST.get('content')
        activity = ActivityBase.objects.get(activity_uuid=activity_uuid)
        card = Cards.objects.create(
            content=content,
            meeting=activity.meeting_structure,
            activity_created_by=activity,
            user_created=request.user
        )
        current_cards = Cards.objects.filter(
            activity_created_by=activity,
            user_created=request.user)
        return Response({'brainstorm_cards': CardSerializer(
            current_cards, many=True).data}, status=200)


class PrioritizationRoute(viewsets.ViewSet):
    def get(self, request):
        activity_uuid = request.GET.get('activity_uuid')
        activity = ActivityBase.objects.get(activity_uuid=activity_uuid)
        current_cards = Cards.objects.filter(
            activity_created_by=activity.data_input, active=True)
        return Response({'brainstorm_cards': CardSerializer(
            current_cards, many=True).data}, status=200)

    def post(self, request):
        activity_uuid = request.data.get('activity_uuid')
        prioritization_activity = ActivityBase.objects.get(
            activity_uuid=activity_uuid)
        if prioritization_activity:
            prioritized_cards = request.data.get('prioritized_cards')

            # backend assumes front-end sends in order that cards should be
            # ranked
            for rank, prioritized_card in enumerate(prioritized_cards):
                PrioritizedCards.objects.create(
                    card_id=prioritized_card['id'],
                    prioritization_activity=prioritization_activity,
                    ranked_by=request.user,
                    rank=rank
                )
            return Response('Success', status=200)


class ForcedRankRoute(viewsets.ViewSet):
    def get(self, request):
        activity_uuid = request.GET.get('activity_uuid')
        activity = ActivityBase.objects.get(activity_uuid=activity_uuid)
        current_cards = Cards.objects.filter(
            activity_created_by=activity.data_input, active=True)
        return Response({'cards': CardSerializer(
            current_cards, many=True).data}, status=200)

    def post(self, request):
        activity_uuid = request.data.get('activity_uuid')
        prioritization_activity = ActivityBase.objects.get(
            activity_uuid=activity_uuid)
        if prioritization_activity:
            prioritized_cards = request.data.get('prioritized_cards')

            # backend assumes front-end sends in order that cards should be
            # ranked
            for rank, prioritized_card in enumerate(prioritized_cards):
                PrioritizedCards.objects.create(
                    card_id=prioritized_card['id'],
                    prioritization_activity=prioritization_activity,
                    ranked_by=request.user,
                    rank=rank
                )
            return Response('Success', status=200)
