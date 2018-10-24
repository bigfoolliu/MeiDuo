#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 21:59
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
用于创建celery对象
"""

from celery import Celery

# 为celery使用django配置文件进行设置,注意下面配置的路径
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MeiDuo.settings.dev'

# 创建celery应用,名字可以随便写
app = Celery('MeiDuo')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务(sms包名)
app.autodiscover_tasks([
    'celery_tasks.sms',
])

