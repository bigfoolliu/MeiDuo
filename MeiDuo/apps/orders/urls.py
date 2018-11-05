#!-*-coding:utf-8-*-
# !@Date: 18-11-5 下午9:18
# !@Author: Liu Rui
# !@github: bigfoolliu
from django.urls import path

from .views import *

urlpatterns = [
    path('settlement/', CartListView.as_view()),
]
