#!-*-coding:utf-8-*-
# !@Date: 2018/10/27 22:18
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
用TimedJSONWebSignatureSerializer可以生成带有有效期的token
服务端使用该token向QQ服务器请求来获取openid
"""
import logging

from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings


logger = logging.getLogger('django')


def dumps(data, expires):
    """
    使用dumps()序列化和对数据签名,生成一个带有过期时间的token
    :param data:
    :param expires:
    :return:
    """
    # 创建TJWSS序列化器对象,利用自定义的密钥和过期时间来创建一个token
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires)
    # dumps()方法生成token,然后加密处理
    result = serializer.dumps(data).decode()

    return result


def loads(data, expires):
    """
    使用loads()来验证签名和反序列化的数据,使用之前自定义的密钥对token进行解密
    :param data:
    :param expires:
    :return:
    """
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires)
    # 解密
    try:
        data_dict = serializer.loads(data)
        return data_dict
    except Exception as e:
        logger.error(e)
        # 超出异常的原因: 超时
        return None
