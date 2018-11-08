#!-*-coding:utf-8-*-
# !@Date: 18-11-7 下午9:14
# !@Author: Liu Rui
# !@github: bigfoolliu
from django.urls import path
from django.urls import re_path

from .views import *

urlpatterns = [
    re_path(r'^orders/(?P<order_id>\d+)/payment/$', AliPayURLView.as_view()),
    path('payment/status/', OrderStatusView.as_view()),
]
