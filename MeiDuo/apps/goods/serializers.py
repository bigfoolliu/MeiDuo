#!-*-coding:utf-8-*-
# !@Date: 18-11-3 下午4:13
# !@Author: Liu Rui
# !@github: bigfoolliu
from rest_framework import serializers

from goods.models import SKU


class SKUSerializer(serializers.ModelSerializer):
    """
    sku序列化器
    """

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_iamge_url', 'comment']
