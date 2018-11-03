#!-*-coding:utf-8-*-
# !@Date: 2018/10/30 21:00
# !@Author: Liu Rui
# !@github: bigfoolliu


from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    re_path(r'^categories/(?P<category_id>\d+)/skus/$', SKUListView.as_view())
]

# 注册搜索的视图url
router = DefaultRouter()
router.register('skus/search', SKUSearchViewsSet, base_name='skus_search')
urlpatterns += router.urls
