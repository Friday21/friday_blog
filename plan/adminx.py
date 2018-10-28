import xadmin

from .models import DailyPlan, YearPlan, MonthPlan, PLAN_TYPE, EventType, WeekPlan
from .admin_forms import DailyPlanAdminForm, MonthPlanAdminForm, YearPlanAdminForm, WeekPlanAdminForm


class DailyPlanAdmin(object):
    form = DailyPlanAdminForm
    list_display = ['title', 'content', 'event_type', 'event_time', 'is_finish', 'finish_status', 'date']
    list_filter = ['date', 'event_type']
    list_editable = ['finish_status', 'is_finish']

    def get_list_queryset(self):
        return super(DailyPlanAdmin, self).get_list_queryset().filter(plan_type=PLAN_TYPE.DAY)


class WeekPlanAdmin(object):
    form = WeekPlanAdminForm
    list_display = ['title', 'content', 'event_type', 'event_time', 'is_finish', 'finish_status', 'week']
    list_filter = ['date', 'event_type']
    list_editable = ['finish_status', 'is_finish']

    def get_list_queryset(self):
        return super(WeekPlanAdmin, self).get_list_queryset().filter(plan_type=PLAN_TYPE.WEEK)


class MonthPlanAdmin(object):
    form = MonthPlanAdminForm
    list_display = ['title', 'content', 'event_type', 'is_finish', 'finish_status', 'month', 'year']
    list_filter = ['year', 'event_type']
    list_editable = ['finish_status', 'is_finish']

    def get_list_queryset(self):
        return super(MonthPlanAdmin, self).get_list_queryset().filter(plan_type=PLAN_TYPE.MONTH)


class YearPlanAdmin(object):
    form = YearPlanAdminForm
    list_display = ['title', 'content', 'event_type', 'is_finish', 'finish_status', 'year']
    list_filter = ['year', 'event_type']
    list_editable = ['finish_status', 'is_finish']

    def get_list_queryset(self):
        return super(YearPlanAdmin, self).get_list_queryset().filter(plan_type=PLAN_TYPE.YEAR)


class EventTypeAdmin(object):
    list_display = ['name']


xadmin.site.register(DailyPlan, DailyPlanAdmin)
xadmin.site.register(WeekPlan, WeekPlanAdmin)
xadmin.site.register(MonthPlan, MonthPlanAdmin)
xadmin.site.register(YearPlan, YearPlanAdmin)
xadmin.site.register(EventType, EventTypeAdmin)