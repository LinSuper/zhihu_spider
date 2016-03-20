# -*- coding: utf-8 -*-
"""This module defines common functions for time convertion
Such as datetime to timestamp, utc time to local time
"""

from calendar import timegm
from datetime import datetime


def utc2local(utc_dt):
    """Convert utc datetime to local datetime"""
    return datetime.fromtimestamp(timegm(utc_dt.timetuple()))


def datetime2timestamp(dt):
    return timegm(dt.timetuple()) * 1000 + dt.microsecond / 1e3


def timestamp2datetime(stamp, to_local=False):
    dt = datetime.utcfromtimestamp(stamp / 1e3)
    if to_local:
        return utc2local(dt)
    return dt


def datetime2string(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
