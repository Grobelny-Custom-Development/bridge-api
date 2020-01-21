from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from uuid import uuid4

from users.models import GenericUser, Company
from bridge.model_utility import TimeStampAbstractMixin

class Component(TimeStampAbstractMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # TODO:: ensure this is working properly
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

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
    components = models.ManyToManyField(Component, through="MeetingComponent")

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
class MeetingComponent(TimeStampAbstractMixin):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    meeting_template = models.ForeignKey(MeetingTemplate, on_delete=models.CASCADE)
    agenda_item =  models.CharField(max_length=255)
    duration = models.DurationField()

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

class Cards(TimeStampAbstractMixin):
    created_by = models.ForeignKey(GenericUser)
    content = models.TextField(blank=True, null=True)
    meeting = models.ForeignKey(MeetingStructure)
    component = models.ForeignKey(MeetingComponent)
    # set by meeting host
    active = models.BooleanField(default=True)