#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 9:10
# !@Author: Liu Rui
# !@github: bigfoolliu
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import *
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('', index),
    re_path('usernames/(?P<username>\w{5,20})/count/', UsernameCountView.as_view()),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/count/', MobileCountView.as_view()),
    path('users/', UserCreateView.as_view()),
    path('authorizations/', obtain_jwt_token),  # 接收username和password,返回一个JSON Web Token
    path('user/', UserDetailView.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', EmailActiveView.as_view()),
    path('browse_histories/', BrowseHistoryView.as_view()),
]

# 为地址的视图集创建url地址
router = DefaultRouter()
router.register('addresses', AddressViewSet, base_name='addresses')
urlpatterns += router.urls
