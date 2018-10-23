from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


# 127.0.0.1/users/
def index(request):
    """
    测试首页
    :param request:
    :return:
    """
    return HttpResponse('ok')
