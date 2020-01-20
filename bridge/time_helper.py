import datetime

import pytz

UTC = pytz.utc
PST = pytz.timezone('America/Los_Angeles')


class TimeHelper:
    def __init__(self):
        pass

    @classmethod
    def get_utc_now_datetime(cls):
        return datetime.datetime.utcnow().replace(tzinfo=UTC)

    @classmethod
    def get_utc_datetime_from_timestamp(cls, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)

    @classmethod
    def convert_utc_datetime_to_pst(cls, utc_datetime_obj):
        return utc_datetime_obj.astimezone(PST)

    @classmethod
    def generate_timedelta(cls, days=0, seconds=0, minutes=0, hours=0):
        timedelta_kwargs = {
            'days': days,
            'seconds': seconds,
            'minutes': minutes,
            'hours': hours
        }
        return datetime.timedelta(**timedelta_kwargs)
