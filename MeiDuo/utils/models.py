#!-*-coding:utf-8-*-
# !@Date: 2018/10/27 15:06
# !@Author: Liu Rui
# !@github: bigfoolliu


from django.db import models


class BaseModel(models.Model):
    """
    用于其他模型类的继承,从而有下方定义字段,并不真的生成一张表
    """
    # 创建时间字段,会自动获取当前时间加入,以后不会改变
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间字段,会自动获取当前时间,以后每次更新都改变
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        # 该属性保证该模型不会生成一张表
        abstract = True

