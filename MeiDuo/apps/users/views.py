from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users import constants
from users.models import User
from users.serializers import UserCreateSerializer, EmailSerializer, UserDetailSerializer, EmailActiveSerializer, \
    AddressSerializer

from rest_framework_jwt.utils import jwt_response_payload_handler
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate

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


# api.meiduo.site:8000/user/
class UserDetailView(RetrieveAPIView):
    """
    显示用户个人中心后端接口
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        """
        RetrieveAPIView视图中封装好的代码，默认是根据主键查询得到的对象
        需求：不根据pk查，而是获取登录的用户,所以直接从request中将user返回
        解决：重写get_object()方法
        :return:
        """
        return self.request.user


# api.meiduo.site:8000/emails/
class EmailView(UpdateAPIView):
    """
    添加邮箱视图接口,即在输入邮箱之后的点击'保存'按钮
    """
    # 声明序列化器
    serializer_class = EmailSerializer
    # 权限判断,要求用户登录才行,request.user才有意义
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        这里根据谁登录来进行更改,不需要query_set查询,所以要对该方法进行重写
        :return:
        """
        return self.request.user


class EmailActiveView(APIView):
    """
    邮箱验证视图接口
    """

    def get(self, request):
        """
        GET请求
        :return:
        """
        serializer = EmailActiveSerializer(data=request.query_params)
        # 验证数据
        if not serializer.is_valid():
            return Response(serializer.errors)

        # 查询当前用户
        user = User.objects.get(pk=serializer.validated_data.get('user_id'))
        # 更改其邮箱验证的状态
        user.email_active = True
        user.save()

        return Response({'message': 'OK'})


class AddressViewSet(ModelViewSet):
    """
    对地址的增删改查视图接口
    retrieve: 默认实现够用
    update: 默认实现够用
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        """
        重新指定查询集,查找的是逻辑上没有删除的
        :return:
        """
        return self.request.user.addresses.filter(is_delete=False)

    def list(self, request, *args, **kwargs):
        """
        查询数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        address_list = self.get_queryset()
        serializer = self.get_serializer(address_list, many=True)

        return Response({
            'user_id': self.request.id,
            'default_address_id': self.request.user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data
        })
