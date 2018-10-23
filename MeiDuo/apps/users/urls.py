#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 9:10
# !@Author: Liu Rui
# !@github: bigfoolliu
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),  # 写空则可以直接通过./users/访问
]
