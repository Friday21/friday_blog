# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from blog_django.tools import EntityState
from blog_django.tools.money_process import to_decimal


class ConsumeType(models.Model):
    name = models.CharField(max_length=128, verbose_name='消费类型')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class BalanceLog(models.Model):
    TYPE_ITEMS = EntityState(
        (1, 'IN', '入账'),
        (2, 'OUT', '消费'),
    )
    TIME_ITEMS = EntityState(
        (1, 'MORNING', '早上'),
        (2, 'NOON', '上午'),
        (3, 'NIGHT', '晚上'),
        (4, 'AFTERNOON', '下午'),
    )
    PAY_METHOD = EntityState(
        (1, "CARD", "银行卡"),
        (2, "WECHAT", '微信'),
        (3, "ALI", "支付宝"),
        (4, "CREDIT", "信用卡"),
        (5, "CASH", "现金"),
    )
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='余额', blank=True)
    type = models.SmallIntegerField(choices=TYPE_ITEMS.items(), default=2, verbose_name='变更类型')
    amt = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='变更金额')
    consume_type = models.ForeignKey(ConsumeType, verbose_name='消费类型', on_delete=models.CASCADE)
    consume_time = models.SmallIntegerField(choices=TIME_ITEMS.items(), verbose_name='消费时间')
    consume_date = models.DateField(verbose_name='消费日期', blank=True)
    extra_info = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    update_time = models.DateTimeField(auto_now=True, verbose_name='变更时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', null=True)
    is_card = models.BooleanField(default=True, verbose_name='是否是银行卡消费')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD.items(), verbose_name='支付方式', default=PAY_METHOD.CARD)

    class Meta:
        verbose_name = verbose_name_plural = '财务变更日志'
        ordering = ['-create_time', '-update_time']

    def save(self, *args, **kwargs):
        if not self.balance:
            if BalanceLog.objects.first():
                pre_balance = BalanceLog.objects.first().balance
            else:
                pre_balance = to_decimal('0.00')

            if self.type == BalanceLog.TYPE_ITEMS.IN:
                self.balance = pre_balance + self.amt
            else:
                self.balance = pre_balance - self.amt
        if not self.consume_date:
            self.consume_date = datetime.now()
        super(BalanceLog, self).save(*args, **kwargs)
