#!-*-coding:utf-8-*-
# !@Date: 2018/10/28 9:59
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
使用jwt对用户生成一个token值
"""
from rest_framework_jwt.settings import api_settings


def generate(user):
    """
    生成函数,对用户生成一个token值
    :param user:
    :return:
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 指定使用配置的payload_handler
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 指定配置的encode_handler
    payload = jwt_payload_handler(user)  # 将用户传入生成payload
    token = jwt_encode_handler(payload)  # 创建token,header.payload.signature

    return token
