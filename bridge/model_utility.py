from django.db import models

from bridge.time_helper import TimeHelper


class TimeStampAbstractMixin(models.Model):
    """
        This abstract mixin is used to add creation_timestamp and updated_timestamp fields to the model this is added to
        also it overrides the save method to update the creation_timestamp and updated_timestamp as needed
    """

    TIMESTAMP_FIELDSETS = ('creation_timestamp', 'updated_timestamp',)
    # timestamps
    creation_timestamp = models.DateTimeField(null=True, blank=True)
    updated_timestamp = models.DateTimeField(
        null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    def update_timestamps(self):
        # get now as UTC
        utc_now = TimeHelper.get_utc_now_datetime()

        # if we have never been saved, then set the creation_timestamp to
        # now(UTC)
        if not self.creation_timestamp:
            self.creation_timestamp = utc_now

        # always overwrite updated_timestamp to now(UTC) with every save
        self.updated_timestamp = utc_now

    def save(self, *args, **kwargs):
        self.update_timestamps()
        super(TimeStampAbstractMixin, self).save(*args, **kwargs)
