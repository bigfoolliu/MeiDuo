#!-*-coding:utf-8-*-
# !@Date: 18-11-5 下午9:46
# !@Author: Liu Rui
# !@github: bigfoolliu
import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods
from users.models import Address


class OrderCreateSerializer(serializers.Serializer):
    """
    创建订单的序列化器
    """
    order_id = serializers.CharField(read_only=True)  # 仅仅用于输出
    address = serializers.IntegerField(write_only=True)  # 仅仅用于输入
    pay_method = serializers.IntegerField(write_only=True)

    def validate_address(self, value):
        """
        验证地址
        :param value:
        :return:
        """
        count = Address.objects.filter(pk=value).count()
        if count <= 0:
            raise serializers.ValidationError('无效的收货地址')
        return value

    def validate_pay_method(self, value):
        """
        验证付款方式
        :param value:
        :return:
        """
        if value not in [1, 2]:
            raise serializers.ValidationError('无效的付款方式')
        return value

    def create(self, validated_data):
        """
        创建订单
        １．创建订单对象
        ２．查询redis中订单的商品编号和数量
        ３．查询商品对象
        ４．遍历这些商品对象，判断其信息,创建订单商品对象
            库存量
            销量
        ５．修改订单的总数量和总金额
        ６．删除redis中的商品信息
        :param validated_data:
        :return:
        """
        """
        在保存订单数据中，涉及到多张表（OrderInfo、OrderGoods、SKU）的数据修改，对这些数据的修改应该是一个整体事务，即要么一起成功，要么一起失败。
        Django中对于数据库的事务，默认每执行一句数据库操作，便会自动提交。我们需要在保存订单中自己控制数据库事务的执行流程。
        """
        # 启用mysql的事务
        with transaction.atomic():
            # 开启事务
            sid = transaction.savepoint()

            # 计算相关字段
            user_id = self.context['request'].user.id
            order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "%09d" % user_id  # 注意日期的格式
            address = validated_data.get('address')
            pay_method = validated_data.get('pay_method')

            print('pay_method:', pay_method)  # TODO:

            # 1.创建订单信息
            total_count = 0
            total_amount = 0
            order = OrderInfo.objects.create(
                order_id=order_id,  # 需要计算
                user_id=user_id,  # user为外键，保存的是id
                address_id=address,
                total_count=0,
                total_amount=0,
                freight=10,
                pay_method=pay_method
            )

            # 2.读取redis中hash的商品id和数量并转换为字典格式
            redis_cli = get_redis_connection('cart')
            cart_redis = redis_cli.hgetall('cart_%d' % user_id)
            cart_dict = {}
            for sku_id, count in cart_redis.items():
                cart_dict[int(sku_id)] = int(count)

            # 读取redis中set中选中的商品编号并转换格式
            sku_ids_redis = redis_cli.smembers('cart_selected_%d' % user_id)
            sku_ids = [int(sku_id) for sku_id in sku_ids_redis]

            # 3.查询商品对象
            skus = SKU.objects.filter(pk__in=sku_ids)  # 查询所有选中的sku

            print('skus:', skus)  # TODO:

            # 4.遍历商品查询其信息
            for sku in skus:
                # 根据购买数量来判断库存是否充足
                count = cart_dict[sku.id]
                if sku.stock < count:  # 库存不够
                    # 回滚事务，将之前的操作取消,使不会当有商品库存不足时仍然可以提交库存足的商品的订单
                    transaction.savepoint_rollback(sid)
                    raise serializers.ValidationError('库存不足')

                # 库存足够，修改库存和商品的销量,并保存到数据库
                sku.stock -= count
                sku.sales += count
                sku.save()

                # 创建订单商品对象
                OrderGoods.objects.create(
                    order_id=order_id,
                    sku_id=sku.id,
                    count=count,
                    price=sku.price,
                )
                # 计算单个sku的总数量和总金额
                total_count += count
                total_amount += count * sku.price

            # 5.修改订单的总数量和总金额
            order.total_count += total_count
            order.total_amount += total_amount
            order.save()

            # 提交事务，从而使得之前的代码生效
            transaction.savepoint_commit(sid)

            # 6.删除redis中的商品信息
            redis_cli.hdel('cart_%d' % user_id, *sku_ids)
            redis_cli.srem('cart_selected_%d' % user_id, *sku_ids)

            # 返回新建的订单对象
            return order
