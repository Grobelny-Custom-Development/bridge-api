from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from uuid import uuid4

from users.models import GenericUser, Company
from bridge.model_utility import TimeStampAbstractMixin

BRAINSTORM = 'brainstormactivity'
FORCED_RANK = 'forcedrankactivity'
GROUPING = 'groupingactivity'
BUCKETING = 'bucketingactivity'
PRIORITIZATION = 'prioritizationactivity'

ACTIVITY_CHOICES = (
    (BRAINSTORM, "Brainstorm Activity"),
    (FORCED_RANK, "Forced Rank Activity"),
    (GROUPING, "Grouping Activity"),
    (BUCKETING, "Bucketing Activity"),
    (PRIORITIZATION, "Prioritization Activity"),
)


class MeetingTemplate(TimeStampAbstractMixin):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'
    INTERVAL_CHOICES = (
        (DAY, 'Day'),
        (WEEK, 'Week'),
        (MONTH, 'Month'),
        (YEAR, 'Year'),
    )
    created_by = models.ForeignKey(GenericUser, related_name='created_by')
    name = models.CharField(max_length=255)
    meeting_type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company_id = models.PositiveIntegerField()
    public = models.BooleanField(default=False)

    # TODO:: figure out interval rules w/ Joe
    interval = models.CharField(choices=INTERVAL_CHOICES, max_length=5)
    interval_count = models.PositiveSmallIntegerField(default=1)

    template_uuid = models.UUIDField(default=uuid4, editable=False)

    def save(self, *args, **kwargs):
        # if we haven't set the uuid then set it now as long as it's not already in the table
        if not self.template_uuid:
            uuid = uuid4()
            while MeetingTemplate.objects.filter(template_uuid=uuid).exists():
                uuid = uuid4()

            self.uuid = uuid
        super(MeetingTemplate, self).save(*args, **kwargs)

    # TODO:: declare duration field that will sum component duration

class MeetingStructure(TimeStampAbstractMixin):
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    meeting_template = models.ForeignKey(MeetingTemplate, related_name='meeting_template')
    meeting_uuid = models.UUIDField(default=uuid4, editable=False)
    host = models.ForeignKey(GenericUser, related_name='host')
    company_id = models.PositiveIntegerField()
    participants = models.ManyToManyField(GenericUser)

    def save(self, *args, **kwargs):
        # if we haven't set the uuid then set it now as long as it's not already in the table
        if not self.meeting_uuid:
            uuid = uuid4()
            while MeetingStructure.objects.filter(meeting_uuid=uuid).exists():
                uuid = uuid4()

            self.uuid = uuid
        super(MeetingStructure, self).save(*args, **kwargs)

class Component(TimeStampAbstractMixin):
    name = models.CharField(max_length=255)
    acitvity_type = models.CharField(choices=ACTIVITY_CHOICES, max_length=100)
    description = models.TextField(blank=True, null=True)
    meeting_template = models.ForeignKey(MeetingTemplate, on_delete=models.CASCADE)
    agenda_item =  models.CharField(max_length=255)
    duration = models.DurationField()
