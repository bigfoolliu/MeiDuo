#!-*-coding:utf-8-*-
# !@Date: 18-11-3 下午4:13
# !@Author: Liu Rui
# !@github: bigfoolliu
from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from goods.models import SKU
from goods.search_index import SKUIndex


class SKUSerializer(serializers.ModelSerializer):
    """
    sku序列化器
    """

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_image_url', 'comment']


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    # 指定数据的序列化器
    object = SKUSerializer(read_only=True)

    class Meta:
        # 索引类的名称可改
        index_classes = [SKUIndex]
        fields = (
            'text',  # 用于接收查询关键字
            'object'  # 用于返回查询结果
        )

