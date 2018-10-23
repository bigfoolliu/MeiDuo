#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 11:15
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
修改Django REST framework的默认异常处理方法，补充处理数据库异常和Redis异常
"""
import logging

from django.db import DatabaseError
from redis import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

# 获取在配置文件中定义的logger,用来记录日志(日志器的名字为django)
logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定义的异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架的原生异常处理方法
    response = drf_exception_handler(exc, context)

    # 如果原生异常处理方法未获取到异常则执行
    if response is None:
        view = context['view']
        # 如果异常为DatabaseError或者RedisError,都输出为同一错误
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response

