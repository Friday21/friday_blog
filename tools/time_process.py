# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

from pytz import timezone
from django.utils.timezone import localtime, utc
from django.conf import settings

TIME_ZONE = settings.TIME_ZONE


def get_local_format_time(utc_time, time_format=settings.LOCAL_TIME_FORMAT):
    """将model中的utc时间转换成指定格式的当地时间字符串"""
    if not utc_time:
        return ''
    local_format_time = datetime.strftime(localtime(utc_time), time_format)
    return local_format_time


def get_utc_format_time(utc_time, time_format=settings.LOCAL_TIME_FORMAT):
    if not utc_time:
        return ''
    return datetime.strftime(utc_time, time_format)


def utc_now_with_tz():
    return datetime.utcnow().replace(tzinfo=utc)


def now_with_tz():
    return localtime(utc_now_with_tz())


def get_utc_month_range(date, time_format='%Y-%m'):
    try:
        month_start = datetime.strptime(date, time_format)
    except (ValueError, TypeError):
        return '', ''
    end_month = month_start.month + 1 if month_start.month < 12 else 1
    year = month_start.year if month_start.month < 12 else month_start.year + 1
    month_end = datetime(year, end_month, 1)
    return month_start.replace(tzinfo=utc), month_end.replace(tzinfo=utc)


def seconds_to_human_show(seconds):
    hours = seconds // 3600
    minutes = seconds // 60 - hours * 60
    if hours > 0:
        remain = "{}时{}分".format(hours, minutes)
    else:
        remain = "{}分".format(minutes)
    return remain


def today_left_seconds():
    """返回当天剩余秒数， 用于设置过期时间为一个自然天(不是24小时)"""
    now = datetime.now()
    left_seconds = 24 * 60 * 60 - now.hour * 60 * 60 - now.minute * 60 - now.second
    return left_seconds


def get_local_yesterday_utc_time():
    """返回utc时区的当地昨天时间"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    local = timezone(TIME_ZONE)
    today_utc = local.localize(today, is_dst=None).astimezone(utc)
    yesterday_utc = local.localize(yesterday, is_dst=None).astimezone(utc)
    return yesterday_utc, today_utc


def get_utc_date_range(date):
    """返回指定日期的utc日期时间范围"""
    date_zero = date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day_zero = date_zero + timedelta(days=1)
    local = timezone(TIME_ZONE)
    date_utc = local.localize(date_zero, is_dst=None).astimezone(utc)
    next_day_utc = local.localize(next_day_zero, is_dst=None).astimezone(utc)
    return date_utc, next_day_utc


def verify_timestamp(timestamp):
    """校验时间戳，判断是否在当前时间的前后4分钟"""
    if not timestamp:
        return False, '参数timestamp为空'
    local_time = int(time.time())
    client_time = int(timestamp)
    if (local_time - settings.FOUR_MINUTES) <= client_time <= (local_time + settings.FOUR_MINUTES):
        return True, ''
    else:
        return False, 'timestamp校验错误'


def trans_local_to_utc(local_time):
    """把当地时间转换成utc时间"""
    local = timezone(TIME_ZONE)
    return local.localize(local_time, is_dst=None).astimezone(utc)


def to_utc_hour(local_hour):
    """把北京时间的小时转为UTC小时"""
    if not isinstance(local_hour, int) or local_hour < 0 or local_hour > 24:
        return None
    if local_hour >= 8:
        return local_hour - 8
    else:
        return local_hour + 16
