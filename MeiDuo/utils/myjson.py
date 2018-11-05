#!-*-coding:utf-8-*-
# !@Date: 18-11-4 下午3:48
# !@Author: Liu Rui
# !@github: bigfoolliu

"""
使用pickle base64两个模块对字典与字符串中的相互转换
"""
import pickle
import base64


def dumps(my_dict):
    """
    将字典转化为字符串
    :param my_dict:
    :return:
    """
    bytes_hex = pickle.dumps(my_dict)  # 字典转换为16进制的字节数据
    bytes_64 = base64.b64encode(bytes_hex)  # 将二进制数字进行加密
    str_result = bytes_64.decode()  # 将二进制格式数据转换为字符串

    return str_result  # 返回字符串


def loads(my_str):
    """
    将字符串转换为字典
    :param my_str:
    :return:
    """
    bytes_64 = my_str.encode()  # 将字符串转换为字节数据

    bytes_hex = base64.b64decode(bytes_64)  # 解密字节数据

    dict_result = pickle.loads(bytes_hex)

    # print('loads() dict_result:', dict_result)  # TODO:

    return dict_result
