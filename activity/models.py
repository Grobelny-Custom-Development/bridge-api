from django.db import models

from users.models import GenericUser, Company
from meetings.models import MeetingStructure, MeetingTemplate, Component
from bridge.model_utility import TimeStampAbstractMixin

class ActivityBase(TimeStampAbstractMixin):
    meeting_structure = models.ForeignKey(MeetingStructure, on_delete=models.CASCADE)
    component = models.ForeignKey(Component)
    class Meta:
        abstract = True

class Cards(TimeStampAbstractMixin):
    content = models.TextField(blank=True, null=True)
    meeting = models.ForeignKey(MeetingStructure)
    # set by meeting host
    active = models.BooleanField(default=True)

class BrainstormActivity(ActivityBase):
    created_cards = models.ManyToManyField(Cards, through="BrainstormCards")

class BrainstormCards(TimeStampAbstractMixin):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    brainstorm_activity = models.ForeignKey(BrainstormActivity, on_delete=models.CASCADE)
    created_by = models.ForeignKey(GenericUser)

# TODO:: potentially create Rank model that both of these inherit from
class PrioritizationActivity(ActivityBase):
    prioritized_cards = models.ManyToManyField(Cards, through="PrioritizedCards")

class PrioritizedCards(TimeStampAbstractMixin):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    prioritization_activity = models.ForeignKey(PrioritizationActivity, on_delete=models.CASCADE)
    ranked_by = models.ForeignKey(GenericUser)
    rank = models.PositiveIntegerField()

class ForcedRankActivity(ActivityBase):
    force_ranked_cards = models.ManyToManyField(Cards, through="ForcedRankedCards")

class ForcedRankedCards(TimeStampAbstractMixin):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    prioritization_activity = models.ForeignKey(ForcedRankActivity, on_delete=models.CASCADE)
    ranked_by = models.ForeignKey(GenericUser)
    rank = models.PositiveIntegerField()

# TODO:: potentially create Group Model that both of these activities inherit from
class GroupingActivity(ActivityBase):
    grouped_cards = models.ManyToManyField(Cards, through="GroupedCards")

class GroupedCards(TimeStampAbstractMixin):
    grouped_by = models.ForeignKey(GenericUser)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    grouping_activity = models.ForeignKey(GroupingActivity, on_delete=models.CASCADE)
    # TODO:: figure out how to identify grouping here

class BucketingActivity(ActivityBase):
    bucketed_cards = models.ManyToManyField(Cards, through="BucketedCards")

class BucketedCards(TimeStampAbstractMixin):
    bucketed_by = models.ForeignKey(GenericUser)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    bucketing_activity = models.ForeignKey(BucketingActivity, on_delete=models.CASCADE)