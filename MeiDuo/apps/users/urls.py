#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 9:10
# !@Author: Liu Rui
# !@github: bigfoolliu
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index),
    re_path('usernames/(?P<username>\w{5,20})/count/', UsernameCountView.as_view()),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/count/', MobileCountView.as_view()),
]
