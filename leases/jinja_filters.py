""" Jinja2 Filters
"""

import pytz
from datetime import datetime, timedelta


def tolocaltime(utc_dt, timezone):
    local_tz = pytz.timezone(timezone)
    local_dt = utc_dt.replace(tzinfo = pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def datetimeformat(value, format_string):
    return value.strftime(format_string)

def secstotimedelta(value):
    return timedelta(seconds=int(value))
