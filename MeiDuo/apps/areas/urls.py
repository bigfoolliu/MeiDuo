#!-*-coding:utf-8-*-
# !@Date: 2018/10/30 9:38
# !@Author: Liu Rui
# !@github: bigfoolliu


from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('areas/', AreaListView.as_view()),
    re_path(r'areas/(?P<pk>\d+)/', AreaRetrieveView.as_view()),
]

# 用视图集来代替上方的两个url

