# coding: utf-8
from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.db import models

from blog_django.tools import EntityState

TIME_ITEM = EntityState(
    (1, 'EARLY_MORNING', '早上'),
    (2, 'MORNING', '上午'),
    (3, 'AFTERNOON', '下午'),
    (4, 'NIGHT', '晚上'),
)

FINISH_STATUS = EntityState(
    (1, 'NO', '非常不满'),
    (2, 'HALF_NO', '不满意'),
    (3, 'HALF_YES', '凑合'),
    (4, 'YES', '满意'),
)

PLAN_TYPE = EntityState(
    (1, 'DAY', '日计划'),
    (4, 'WEEK', '周计划'),
    (2, 'MONTH', '月计划'),
    (3, 'YEAR', '年计划'),
)

MONTH_ITEM = EntityState(
    (1, 'JAN', '一月'),
    (2, 'FEB', '二月'),
    (3, 'MAT', '三月'),
    (4, 'APR', '四月'),
    (5, 'MAY', '五月'),
    (6, 'JUN', '六月'),
    (7, 'JUL', '七月'),
    (8, 'AUG', '八月'),
    (9, 'SEP', '九月'),
    (10, 'OCT', '十月'),
    (11, 'NOV', '十一月'),
    (12, 'DEC', '十二月'),
)

WEEK_ITEM = EntityState(
    (1, 'FIRST', '第一周'),
    (2, 'SECOND', '第二周'),
    (3, 'THIRD', '第三周'),
    (4, 'FOURTH', '第四周'),
    (5, 'FIFTH', '第五周'),
)


class EventType(models.Model):
    name = models.CharField(max_length=256, verbose_name='类型')

    class Meta:
        verbose_name = verbose_name_plural = '事件类型'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Event(models.Model):
    plan_type = models.SmallIntegerField(choices=PLAN_TYPE.items(), default=1, verbose_name='计划类型')
    event_type = models.ForeignKey(EventType, verbose_name='内容分类', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='计划名称')
    content = models.TextField(max_length=1024, verbose_name='计划内容')
    finish_status = models.SmallIntegerField(choices=FINISH_STATUS.items(), default=1, verbose_name='满意程度')
    is_finish = models.BooleanField(verbose_name='是否完成', default=False)
    event_time = models.SmallIntegerField(choices=TIME_ITEM.items(), verbose_name='计划时间段', null=True, blank=True)
    date = models.DateField(verbose_name='计划日期', null=True, blank=True)
    week = models.SmallIntegerField(choices=WEEK_ITEM.items(), verbose_name='周', null=True, blank=True)
    month = models.SmallIntegerField(choices=MONTH_ITEM.items(), verbose_name='月份', null=True, blank=True)
    year = models.SmallIntegerField(verbose_name='年份', default=2018, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now().date()
        if not self.month:
            self.month = self.date.month
        if not self.year:
            self.year = self.date.year
        if not self.week:
            weekday = self.date.weekday()
            week = 1
            if (self.date - timedelta(days=weekday)).month != self.month:
                self.month = (self.date - timedelta(days=weekday)).month
            for i in range(1, 6):
                if (self.date - timedelta(days=(weekday + 7*i))).month == self.month:
                    week += 1
            self.week = week
        super(Event, self).save(*args, **kwargs)


class DailyPlan(Event):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '日计划'


class WeekPlan(Event):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '周计划'


class MonthPlan(Event):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '月计划'


class YearPlan(Event):
    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = '年计划'