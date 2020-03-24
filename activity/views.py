import json
import ast
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from activity.models import ActivityBase, Buckets, BucketedCards
from meetings.models import MeetingStructure


class BucketingRoute(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get_buckets(self, request):
        activity_uuid = request.GET.get('activity_uuid')
        bucketing_activity = ActivityBase.objects.get(
            activity_uuid=activity_uuid)
        buckets = Buckets.objects.filter(bucketing_activity=bucketing_activity)

        return Response({'buckets': buckets.values()}, status=200)

    def post(self, request):
        bucket_submission = request.data.get('submission')
        # TODO:: change this to activity_uuid
        activity_uuid = request.data.get('activity_uuid')
        bucketing_activity = ActivityBase.objects.get(
            activity_uuid=activity_uuid)

        bucket_dict = bucket_submission
        for bucket_id in bucket_dict.keys():
            for card in json.loads(bucket_dict[bucket_id]):
                BucketedCards.objects.create(
                    card_id=card['id'],
                    bucketing_activity=bucketing_activity,
                    bucketed_by=request.user,
                    bucket_id=bucket_id
                )

        return Response({'success': 'success'}, status=200)
