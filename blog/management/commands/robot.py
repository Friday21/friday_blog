import re
import random
from datetime import datetime, timedelta
from decimal import Decimal

import itchat
from django.core.management import BaseCommand

from bill.models import BalanceLog, ConsumeType
from plan.models import DailyPlan, EventType, PLAN_TYPE, TIME_ITEM
from blog.models import AccessLog


HELP = """可用命令如下：
    （今天）上午消费5元 超市 （微信）
    今天晚上计划 学习 机器学习看一节
    今天[昨天|7天内]访客人数
    """

UNKNOWN = ["I don't get it", "你说的好高深， 我没懂诶", "我没明白你说的是什么", "你说啥？俺没听见",
           "0x0x0x0x0x, 我乱码了， 没搞懂你说的意思", "你说的话入木三分， 超出了我的理解范围"]


@itchat.msg_register(itchat.content.TEXT)
def text_reply(req):
    message = req.text
    if req['ToUserName'] == 'filehelper' or \
            req['FromUserName'] == '@67356da109edda60000bcf5fdbba0d1a4053ea47d579f720b9c17805a7e43e47':
        # 记录消费信息、日报
        if message.startswith('help') or message.startswith('帮助'):
            msg = HELP
        elif re.match('^[今天|昨天|今日|昨日|today|yesterday]{0,2}[早上|上午|下午|晚上]{1,2}消费.*', message):
            try:
                msg = handle_consume(message)
            except Exception as e:
                msg = '格式不正确，exception:{}, ex:今天上午消费5元 超市 微信'.format(e)
        elif re.match('^[今天|今日|明天|明日]{0,2}[早上|上午|下午|晚上]{1,2}计划.*', message):
            try:
                msg = handle_daily_plan(message)
            except Exception as e:
                msg = '格式不正确，exception:{}, ex:今天晚上计划 学习 机器学习看一节'.format(e)
        elif re.match('^[今天|昨天|\d天内]{1,2}访客人数.*', message):
            try:
                msg = handle_visit_count(message)
            except Exception as e:
                msg = '格式不正确，exception:{}, ex:[今天|昨天|7天内]访客人数'.format(e)
        else:
            msg = random.choice(UNKNOWN)
        if req['ToUserName'] == 'filehelper':
            itchat.send(msg, toUserName='filehelper')
        else:
            return msg


def handle_consume(message):
    if '上午' in message:
        time_item = BalanceLog.TIME_ITEMS.NOON
    elif '早上' in message:
        time_item = BalanceLog.TIME_ITEMS.MORNING
    elif '下午' in message:
        time_item = BalanceLog.TIME_ITEMS.AFTERNOON
    else:
        time_item = BalanceLog.TIME_ITEMS.NIGHT
    consume_date = datetime.now()
    if '昨天' in message or '昨日' in message or 'yesterday' in message:
        consume_date = datetime.now() - timedelta(days=1)
    consume_date = consume_date.date()
    num = re.findall('^[今天|昨天|今日|昨日|today|yesterday]{0,2}[早上|上午|下午|晚上]{1,2}消费(\d)元.*', message)
    num = int(num[0])
    _, consume_type, pay_method = message.split()
    consume_type, _ = ConsumeType.objects.get_or_create(name=consume_type)
    if '微信' in pay_method:
        PAY_METHOD = BalanceLog.PAY_METHOD.WECHAT
    elif '支付宝' in pay_method:
        PAY_METHOD = BalanceLog.PAY_METHOD.ALI
    elif '现金' in pay_method:
        PAY_METHOD = BalanceLog.PAY_METHOD.CASH
    elif '信用卡' in pay_method:
        PAY_METHOD = BalanceLog.PAY_METHOD.CREDIT
    else:
        PAY_METHOD = BalanceLog.PAY_METHOD.CARD
    balance_log = BalanceLog(amt=Decimal(num), consume_date=consume_date, consume_type=consume_type,
                             pay_method=PAY_METHOD, consume_time=time_item)
    balance_log.save()
    return 'copy'


def handle_daily_plan(message):
    plan_time, event_type, content = message.split()
    if '早上' in plan_time:
        event_time = TIME_ITEM.EARLY_MORNING
    elif '上午' in plan_time:
        event_time = TIME_ITEM.MORNING
    elif '下午' in plan_time:
        event_time = TIME_ITEM.AFTERNOON
    else:
        event_time = TIME_ITEM.NIGHT

    date = datetime.now()
    if '明天' in plan_time or '明日' in plan_time:
        date = date - timedelta(days=1)
    date = date.date()

    event_type, _ = EventType.objects.get_or_create()
    plan = DailyPlan(plan_type=PLAN_TYPE.DAY, event_type=event_type, title=content, content=content,
                     date=date, event_time=event_time)
    plan.save()
    return 'copy'


def handle_visit_count(message):
    from_time = datetime.now().replace(hour=0, minute=0)
    if '昨天' in message:
        from_time = from_time - timedelta(days=1)
    elif '今天' not in message and '今日' not in message:
        days = int(re.findall('(\d+)天内', message)[0])
        from_time = from_time - timedelta(days=days)
    visit_count = AccessLog.objects.filter(access_time__gte=from_time).count()
    return '{}'.format(visit_count)


class Command(BaseCommand):
    def handle(self, *args, **options):
        itchat.auto_login()
        itchat.run()
