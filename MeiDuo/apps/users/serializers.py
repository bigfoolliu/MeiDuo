#!-*-coding:utf-8-*-
# !@Date: 2018/10/24 20:30
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
存放users应用所需要的序列化器
"""
import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User


class UserCreateSerializer(serializers.Serializer):
    """
    用户创建需要的序列化器
    """
    # 定义属性
    id = serializers.IntegerField(read_only=True)  # 只输出到客户端,不接收
    token = serializers.CharField(read_only=True)  # 想要token作为属性,需要定义
    username = serializers.CharField(
        min_length=5,
        max_length=20,
        error_messages={
            'min_length': '用户名必须为5-20个字符',
            'max_length': '用户名必须为5-20个字符'
        }
    )
    password = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码必须为8-20个字符',
            'max_length': '密码名必须为8-20个字符'
        },
        write_only=True  # 只从客户端接收,不输出
    )
    password2 = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码必须为8-20个字符',
            'max_length': '密码名必须为8-20个字符'
        },
        write_only=True  # 只从客户端接收,不输出
    )
    sms_code = serializers.IntegerField(write_only=True)
    mobile = serializers.CharField()
    allow = serializers.BooleanField(write_only=True)

    def validate(self, attrs):
        """
        验证属性(多属性与单独的属性在一起验证)
        :param attrs:
        :return:
        """
        # 获取所有需要的参数
        username = attrs.get('username')
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        sms_code_request = attrs.get('sms_code')  # request中的sms_code
        allow = attrs.get('allow')

        # 1. 验证用户名是否重复
        count = User.objects.filter(username=username).count()
        if count > 0:
            raise serializers.ValidationError('该用户名已注册')

        # 2. 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式错误')
        # 验证手机号是否重复
        count = User.objects.filter(mobile=mobile).count()
        if count > 0:
            raise serializers.ValidationError('手机号已经注册')

        # 3. 判断两次密码是否一致
        if password != password2:
            raise serializers.ValidationError('两次密码输入不一致')

        # 4. 判断短信验证码正确性
        redis_cli = get_redis_connection('sms_code')  # 获取redis连接
        sms_code_redis = redis_cli.get('sms_code_' + mobile)  # 获取redis中存储的sms_code(过期则为None)
        if sms_code_redis is None:
            raise serializers.ValidationError('短信验证码过期')
        # 将redis中的验证码删除
        redis_cli.delete('sms_code_' + mobile)
        if int(sms_code_request) != int(sms_code_redis):  # redis中取出来的sms_code默认为字节类型,可以int强制转换
            raise serializers.ValidationError('短信验证码错误')

        # 5. 判断是否同意协议
        if not allow:
            raise serializers.ValidationError('请同意协议')

        return attrs

    def create(self, validated_data):
        """
        创建一个用户
        :param validated_data: 经过验证后的数据
        :return:
        """
        user = User()
        user.username = validated_data.get('username')
        user.mobile = validated_data.get('mobile')
        # 用户的密码需要加密,所以需要调用函数进行加密
        user.set_password(validated_data.get('password'))
        user.save()

        """
        利用jwt生成token值,并将其作为user的属性添加至用户
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)  # 创建token,header.payload.signature
        user.token = token  # 将token作为属性赋给用户

        return user

