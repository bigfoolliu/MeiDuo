#!-*-coding:utf-8-*-
# !@Date: 2018/10/30 21:00
# !@Author: Liu Rui
# !@github: bigfoolliu


from django.urls import path
from django.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^categories/(?P<category_id>\d+)/skus/$', SKUListView.as_view())
]
