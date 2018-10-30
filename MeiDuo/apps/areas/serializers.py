#!-*-coding:utf-8-*-
# !@Date: 2018/10/30 10:27
# !@Author: Liu Rui
# !@github: bigfoolliu
from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    省份地区序列化器
    """

    class Meta:
        model = Area
        fields = ['id', 'name']  # 序列化时输出两个字段


class AreaSubSerializer(serializers.ModelSerializer):
    """
    下辖区域序列化器
    """
    # subs为关系属性,默认以pk输出,可以指定输出方式
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
