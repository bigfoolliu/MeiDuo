from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from carts.utils import merge_cookie_to_redis
from goods.models import SKU
from goods.serializers import SKUSerializer
from users import constants
from users.models import User
from users.serializers import UserCreateSerializer, EmailSerializer, UserDetailSerializer, EmailActiveSerializer, \
    AddressSerializer, BrowseHistorySerializer

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
    update: 默认实现够用,不需要修改
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
            'user_id': self.request.user.id,
            'default_address_id': self.request.user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """
        重写删除方法,因为默认的方式是接收pk,删除也是物理删除
        此处应该实现逻辑删除
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 根据主键查到当前要删除的地址
        address = self.get_object()
        # 实现逻辑删除
        address.is_delete = True
        address.save()

        # 返回响应,不需要信息,只需要返回一个状态码
        return Response(status=204)

    """
    下方的 title 和 status 都是进行修改操作,即请求为 put 请求,与原有的冲突
    为了解决冲突,所有使用 ModelViewSet 的 action 来新增方法
    """

    # 修改标题===>****/pk/title/------put
    # 如果没有detail=False=====>*****/title/
    # addresses/(?P<pk>[^/.]+)/title/$ [name='addresses-title']
    @action(methods=['PUT'], detail=True)
    def title(self, request, pk):
        """
        修改地址的标题
        :param request:
        :param pk:
        :return:
        """
        # 根据主键查询收货地址
        address = self.get_object()
        # 接收数据修改标题属性
        address.title = request.data.get('title')
        address.save()
        return Response({'title': address.title})

    # 设置默认收货地址===>^ ^addresses/(?P<pk>[^/.]+)/status/$ [name='addresses-status']
    @action(methods=['PUT'], detail=True)
    def status(self, request, pk):
        """
        将地址设置为默认地址
        :param request:
        :param pk:
        :return:
        """
        # 查找当前登录的用户
        user = request.user  # 此处之所以能这么用是因为ModelViewSet封装的
        # 将当前地址设置为默认收货地址
        user.default_address_id = pk
        user.save()
        return Response({'message': 'OK'})


class BrowseHistoryView(generics.ListCreateAPIView):
    """
    浏览历史视图
    """
    permission_classes = [IsAuthenticated]  # 登陆的用户才能有浏览历史

    def get_serializer_class(self):
        """
        根据不同的请求方式来指定序列化器
        :return:
        """
        if self.request.method == 'GET':
            return SKUSerializer
        else:
            return BrowseHistorySerializer

    def get_queryset(self):
        """
        指定查询集,即存储在redis数据库中的对应该用户的数据
        :return:
        """
        redis_cli = get_redis_connection('history')
        key = 'history_%d' % self.request.user.id
        # 找到所有浏览的sku的sku_id
        sku_ids = redis_cli.lrange(key, 0, -1)
        # 遍历列表,根据sku_id查询所有的商品对象
        skus = []
        for sku_id in sku_ids:
            skus.append(SKU.objects.get(pk=int(sku_id)))  # redis中的数据均为字节需转换格式

        return skus


class LoginView(ObtainJSONWebToken):
    """
    继承jwt中的ObtainJSONWebToken类，但是不改变其原始的功能，继续完成登录验证功能
    在登录功能之后添加其他的功能
    """

    def post(self, request, *args, **kwargs):
        """
        重写登录的方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:  # 用户登录成功,注意这里的状态码为整型

            print('用户登录成功')  # TODO:

            # 获取用户的编号，可以从request或者登录成功的response中获取
            user_id = response.data.get('user_id')  # response.data为一个字典
            # 执行购物车合并操作
            response = merge_cookie_to_redis(request, user_id, response)

        return response
