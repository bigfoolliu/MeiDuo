#!-*-coding:utf-8-*-
# !@Date: 2018/10/26 19:56
# !@Author: Liu Rui
# !@github: bigfoolliu


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
