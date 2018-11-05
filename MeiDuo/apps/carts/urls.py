#!-*-coding:utf-8-*-
# !@Date: 18-11-4 下午3:58
# !@Author: Liu Rui
# !@github: bigfoolliu


from django.urls import path
from .views import *


urlpatterns = [
    path('cart/', CartView.as_view()),
    path('cart/selection/', CartSelectView.as_view()),
]
