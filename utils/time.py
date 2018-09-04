import pytz
import datetime
from django.conf import settings


def add_timezone(dt_naive: datetime.datetime):
    if dt_naive.tzinfo:
        dt_naive.replace(tzinfo=None)
    local_tz = pytz.timezone(settings.TIME_ZONE)
    dt_aware = local_tz.localize(dt_naive)
    return dt_aware
