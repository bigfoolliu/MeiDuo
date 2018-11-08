from django.db import models

# Create your models here.
from MeiDuo.utils.models import BaseModel


class Payment(BaseModel):
    """
    支付类
    """
    order = models.ForeignKey('orders.OrderInfo', verbose_name='订单信息', on_delete=None)
    trade_no = models.CharField(max_length=200, verbose_name='支付流水号')

    class Meta:
        db_table = 'tb_payments'
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name

