from django import forms

from .models import DailyPlan, MonthPlan, YearPlan, WeekPlan


class DailyPlanAdminForm(forms.ModelForm):

    class Meta:
        model = DailyPlan
        exclude = ['created_time', 'update_time']


class WeekPlanAdminForm(forms.ModelForm):

    class Meta:
        model = WeekPlan
        exclude = ['created_time', 'update_time', 'event_time', 'date']


class MonthPlanAdminForm(forms.ModelForm):

    class Meta:
        model = MonthPlan
        exclude = ['created_time', 'update_time', 'event_time', 'date']


class YearPlanAdminForm(forms.ModelForm):

    class Meta:
        model = YearPlan
        exclude = ['month', 'created_time', 'update_time', 'event_time', 'date']
