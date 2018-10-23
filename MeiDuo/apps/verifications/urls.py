#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 20:37
# !@Author: Liu Rui
# !@github: bigfoolliu
from django.urls import re_path
from .views import *

urlpatterns = [
    re_path('sms_code/(?P<mobile>1[3-9]\d{9})/', SMSCodeView.as_view()),  # 注意当路径比较复杂需要正则表达式时使用re_path
]
