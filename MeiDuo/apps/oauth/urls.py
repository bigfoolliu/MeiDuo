#!-*-coding:utf-8-*-
# !@Date: 2018/10/27 9:36
# !@Author: Liu Rui
# !@github: bigfoolliu


from django.urls import path
from .views import *


urlpatterns = [
    path('qq/authorization/', QQurlView.as_view()),
    path('qq/user/', QQLoginView.as_view()),
]
