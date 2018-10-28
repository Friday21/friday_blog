# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.utils.timezone import localtime


def get_local_format_time(utc_time, time_format='%Y-%m-%d %H:%M'):
    if not utc_time:
        return ''
    local_format_time = datetime.strftime(localtime(utc_time), time_format)
    return local_format_time