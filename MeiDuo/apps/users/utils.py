#!-*-coding:utf-8-*-
# !@Date: 2018/10/26 19:56
# !@Author: Liu Rui
# !@github: bigfoolliu
import re

from django.contrib.auth.backends import ModelBackend
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    重新定义jwt认证成功返回数据
    该方法默认只返回token一个值
    需要在配置文件中进行更改配置,让其指向该处理函数
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class MyModelBackend(ModelBackend):
    """
    继承ModelBackend,重写其中的authenticate方法
    同时要更改配置中我们自定义的认证后端
    JWT扩展的登录视图收到用户名与密码时,调用Django的认证系统中提供的authenticate()来检查用户名与密码是否正确.
    通过修改Django认证系统的认证后端（主要是authenticate方法）来支持登录账号既可以是用户名也可以是手机号.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        用户认证方法重写,使可以同时支持用户名和手机号登录
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        try:
            # 如果满足手机号的正则表达式则认为是手机号登录(有点点不太合理!)
            if re.match(r'^1[3-9]\d{9}$', username):
                user = User.objects.get(mobile=username)
            else:
                user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return None

        # 判断密码正确性
        if user.check_password(password):
            # 最后需要将返回用户对象(和原始authenticate函数要一致)
            return user
        else:
            return None

