from django.db import models
from uuid import uuid4
from users.models import GenericUser, Company
from meetings.models import MeetingStructure, MeetingTemplate, Component
from bridge.model_utility import TimeStampAbstractMixin


class ActivityBase(TimeStampAbstractMixin):
    meeting_structure = models.ForeignKey(
        MeetingStructure, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    activity_uuid = models.UUIDField(default=uuid4, editable=False)
    # data_input activity - might have to be circular input
    data_input = models.ForeignKey(
        "ActivityBase",
        null=True,
        on_delete=models.CASCADE)

# Brainstorm/ Other activities can spawn cards


class Cards(TimeStampAbstractMixin):
    content = models.TextField(blank=True, null=True)
    meeting = models.ForeignKey(MeetingStructure)
    # set by meeting host
    active = models.BooleanField(default=True)
    activity_created_by = models.ForeignKey(
        ActivityBase, on_delete=models.CASCADE)
    user_created = models.ForeignKey(GenericUser, on_delete=models.CASCADE)


class PrioritizedCards(TimeStampAbstractMixin):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    prioritization_activity = models.ForeignKey(
        ActivityBase, on_delete=models.CASCADE)
    ranked_by = models.ForeignKey(GenericUser)
    rank = models.PositiveIntegerField()


class ForcedRankedCards(TimeStampAbstractMixin):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    prioritization_activity = models.ForeignKey(
        ActivityBase, on_delete=models.CASCADE)
    ranked_by = models.ForeignKey(GenericUser)
    rank = models.PositiveIntegerField()


class Buckets(TimeStampAbstractMixin):
    name = models.CharField(max_length=25)
    bucketing_activity = models.ForeignKey(
        ActivityBase, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        GenericUser,
        default=None,
        on_delete=models.CASCADE)


class BucketedCards(TimeStampAbstractMixin):
    bucketed_by = models.ForeignKey(GenericUser)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    bucketing_activity = models.ForeignKey(
        ActivityBase, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Buckets, default=None, on_delete=models.CASCADE)
