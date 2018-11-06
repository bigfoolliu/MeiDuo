from django.contrib import admin

# Register your models here.
from orders.models import OrderInfo, OrderGoods

admin.site.register(OrderInfo)  # 后台注册订单信息
admin.site.register(OrderGoods)  # 后台注册订单的商品信息
