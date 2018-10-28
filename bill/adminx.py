import xadmin

from .adminforms import BalanceLogAdminForm
from .models import BalanceLog, ConsumeType


class BalanceLogAdmin(object):
    form = BalanceLogAdminForm
    list_display = ['balance', 'amt', 'type', 'consume_type', 'consume_time', 'consume_date', 'extra_info']
    list_editable = ['extra_info']


class ConsumeTypeAdmin(object):
    list_display = ['name']


xadmin.site.register(BalanceLog, BalanceLogAdmin)
xadmin.site.register(ConsumeType, ConsumeTypeAdmin)