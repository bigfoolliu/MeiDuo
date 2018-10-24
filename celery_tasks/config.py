#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 21:57
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
用celery事项框架异步的配置文件
"""

# 指定代理人,此处redis的数据库开始倒着用
broker_url = 'redis://127.0.0.1:6379/15'
