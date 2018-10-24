from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from users.models import User
from users.serializers import UserCreateSerializer

# Create your views here.


# api.meiduo.site:8000/
def index(request):
    """
    测试首页
    :param request:
    :return:
    """
    return HttpResponse('ok')


# api.meiduo.site:8000/usernames/(?P<username>\w{5,20})/count/
class UsernameCountView(APIView):
    """
    查询用户名为username的用户数量
    """

    def get(self, request, username):
        """
        GET请求
        :param request:
        :param username:
        :return:
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


# api.meiduo.site:8000/mobiles/(?P<mobile>1[3-9]\d{9})/count/
class MobileCountView(APIView):
    """
    验证手机号是否已经存在
    """

    def get(self, request, mobile):
        """
        查询手机号的个数
        :param request:
        :param mobile:
        :return:
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# api.meiduo.site:8000/users/
class UserCreateView(CreateAPIView):
    """
    创建用户视图,注册的具体实现
    使用序列化器来简化
    """
    serializer_class = UserCreateSerializer

