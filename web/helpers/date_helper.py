# -*- coding: utf-8 -*-
import calendar
from datetime import datetime

import pytz
from pytz import timezone


def get_current_date(format='%Y-%m-%d %H:%M:%S'):
    client_time = datetime.utcnow()
    if format:
        client_time = client_time.strftime(format)
    return client_time


def get_current_utc():
    return calendar.timegm(datetime.utcnow().utctimetuple())


def to_utc(date, tz):
    tz = timezone(tz)
    utc = pytz.timezone('UTC')
    d_tz = tz.normalize(tz.localize(date))
    d_utc = d_tz.astimezone(utc).replace(tzinfo=None)
    return d_utc


def from_utc(date, tz):
    tz = timezone(tz)
    utc = pytz.timezone('UTC')
    d_tz = utc.normalize(utc.localize(date))
    localetime = d_tz.astimezone(tz)
    return localetime


def convert_date_to_utc(date, tz, input, output):
    conv = datetime.strptime(date, input)
    return to_utc(conv, tz).strftime(output)


def convert_date_from_utc(date, tz, input, output):
    conv = datetime.strptime(date, input)
    return from_utc(conv, tz).strftime(output)
