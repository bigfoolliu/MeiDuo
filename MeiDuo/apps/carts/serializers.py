#!-*-coding:utf-8-*-
# !@Date: 18-11-4 下午3:59
# !@Author: Liu Rui
# !@github: bigfoolliu
from rest_framework import serializers

from goods.models import SKU


class CartAddSerializer(serializers.Serializer):
    """
    将商品添加至购物车的序列化器
    """
    sku_id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1, max_value=5)  # 加入购物车的商品数量
    selected = serializers.BooleanField(default=True, required=False)

    def validate_sku_id(self, value):
        """
        验证sku_id
        :return:
        """
        count = SKU.objects.filter(pk=value).count()
        if count <= 0:
            raise serializers.ValidationError('无效的商品编号')
        return value


class CartSerializer(serializers.ModelSerializer):
    """
    查找购物车商品的序列化器
    """
    count = serializers.IntegerField()
    selected = serializers.BooleanField()

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_image_url', 'count', 'selected']


class CartDeleteSerializer(serializers.Serializer):
    """
    删除购物车商品序列化器
    """
    sku_id = serializers.IntegerField()

    def validate_sku_id(self, value):
        """
        验证sku_id
        :param value:
        :return:
        """
        count = SKU.objects.filter(pk=value).count()
        if count <= 0:
            raise serializers.ValidationError('无效的商品编号')
        return value


class CartSelectSerializer(serializers.Serializer):
    """
    选取购物车商品序列化器
    """
    selected = serializers.BooleanField()
