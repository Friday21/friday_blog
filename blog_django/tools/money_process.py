# coding: utf-8

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


def to_decimal(money):
    """
    1 --> Decimal('1.00')
    1.1 --> Decimal('1.10')
    1.222 --> Decimal('1.22')
    '1.22' --> Decimal('1.22')
    '1' ——> Decimal('1.00')
    """
    if isinstance(money, int):  # 1
        money = str(money) + '.00'
    elif not isinstance(money, str):
        money = str(money)

    if '.' not in money:  # '1'
        money += '.00'
    elif len(money.split('.')[1]) > 2:
        logger.error('金额转换精度错误， 金额：{}'.format(money))
        money = money.split('.')[0] + '.' + money.split('.')[1][:2]
    elif len(money.split('.')[1]) < 2:
        money += '0' * (2 - len(money.split('.')[1]))
    return Decimal(money)


def decimal_to_str(money):
    money_str = str(to_decimal(money))
    if '.' not in money_str:
        money_str += '.00'
    elif len(money_str.split('.')[-1]) < 2:
        money_str += '0' * (2 - len(money.split('.')[1]))
    return money_str
