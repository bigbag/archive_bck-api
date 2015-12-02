# -*- coding: utf-8 -*-
import calendar
import time
from datetime import datetime, timedelta

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


def to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def to_unixtime(date):
    return int(calendar.timegm(date.timetuple()))


def get_date_interval(timestamp, period='day', tz='UTC'):
    search_date = datetime.fromtimestamp(timestamp)

    start = datetime(search_date.year,
                     search_date.month,
                     search_date.day, 0, 0, 0)
    stop = datetime(search_date.year,
                    search_date.month,
                    search_date.day, 23, 59, 59)
    if period == 'week':
        day_of_week = search_date.weekday()
        start_delta = timedelta(days=day_of_week)
        start_date = search_date - start_delta
        stop_delta = timedelta(days=6 - day_of_week)
        stop_date = search_date + stop_delta

        start = datetime(start_date.year,
                         start_date.month,
                         start_date.day, 0, 0, 0)
        stop = datetime(stop_date.year,
                        stop_date.month,
                        stop_date.day, 23, 59, 59)
    elif period == 'month':
        last_day = calendar.monthrange(search_date.year, search_date.month)[1]
        start = datetime(search_date.year,
                         search_date.month,
                         1, 0, 0, 0)
        stop = datetime(search_date.year, search_date.month,
                        last_day, 23, 59, 59)

    return (to_utc(start, tz).replace(tzinfo=None),
            to_utc(stop, tz).replace(tzinfo=None))
