#!-*-coding:utf-8-*-
# !@Date: 2018/10/28 10:05
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
进行将qq账号绑定原有账户的序列化器
"""
import logging

from rest_framework import serializers

from oauth import constants
from oauth.models import QQUser
from users.models import User
from MeiDuo.utils import tjws


logger = logging.getLogger('django')


class QQBindSerializer(serializers.Serializer):
    """
    绑定qq序列化器类
    """
    # 定义属性
    mobile = serializers.CharField()
    password = serializers.CharField()
    sms_code = serializers.CharField()
    access_token = serializers.CharField()

    # 验证
    def validate(self, attrs):
        """
        验证绑定时提交的数据的正确性
        :param attrs:
        :return:
        """
        # 对access_token进行解密
        data_dict = tjws.loads(attrs.get('access_token'), constants.BIND_TOKEN_EXPIRES)
        # 判断解密数据是否过期
        if data_dict is None:
            raise serializers.ValidationError('access_token过期')
        # 获取openid
        openid = data_dict.get('openid')
        # 将获取到的openid加入字典
        attrs['openid'] = openid

        return attrs

    def create(self, validated_data):
        """
        新用户,首次使用qq登录,则创建一个用户
        :param validated_data:
        :return:
        """
        # 获取填入的数据
        mobile = validated_data.get('mobile')
        openid = validated_data.get('openid')
        password = validated_data.get('password')

        # 查询手机号是否对应着一个用户
        try:
            user = User.objects.get(mobile=mobile)
        except Exception as e:
            logger.error(e)
            # 没有对应一个用户,所以创建一个用户
            user = User()
            user.mobile = mobile
            user.username = mobile
            user.set_password(password)
            user.save()
        else:
            # 如果对应一个用户,则进行密码对比
            if not user.check_password(password):
                raise serializers.ValidationError('此手机号已经被使用')
        # 绑定: 创建QQUser对象
        qquser = QQUser()
        qquser.openid = openid
        qquser.user = user
        qquser.save()

        return qquser


class EmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """

    class Meta:
        model = User
        fields = ['email']

    def update(self, instance, validated_data):
        """
        修改用户的邮箱状态
        :param instance:
        :param validated_data:
        :return:
        """
        pass


class EmailActiveSerializer(serializers.Serializer):
    """
    邮箱激活序列化器
    """
    pass

