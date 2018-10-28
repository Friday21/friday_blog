from django import forms

from .models import BalanceLog


class BalanceLogAdminForm(forms.ModelForm):

    class Meta:
        model = BalanceLog
        exclude = ['balance', 'is_card']

