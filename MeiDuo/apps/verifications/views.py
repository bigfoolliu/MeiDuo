import random

from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from utils.ytx_sdk.sendSMS import CCP
from verifications import constants


class SMSCodeView(APIView):
    """
    短信验证视图类
    """
    def get(self, request, mobile):
        """
        限制最少每隔60s才向一个手机号发送短信验证码
        1. 判断60s内是否已经发送过短信
        2. 未发送短信则生成6位数的随机短信验证码
        3. 使用云通讯发送短信
        4. 响应
        :param request:
        :param mobile: 路径中携带的手机号
        :return:
        """
        # 获取redis的连接: 从配置中的cache处,根据名称获取与redis的连接,从而使用redis_cli直接操作redis数据库
        redis_cli = get_redis_connection('sms_code')

        # 如果60秒内向指定手机发送短信,则报异常
        if redis_cli.get('sms_flag_' + mobile):
            raise serializers.ValidationError('向该手机发送短信过于频繁!')

        # 未发送过短信则生成随机6位数短信验证码
        code = random.randint(100000, 999999)

        # 将验证码保存至redis,同时携带一个发送的标记
        # 使用"管道方式"来交互redis,因为是多个redis命令,使用pipeline可以优化
        redis_pipeline = redis_cli.pipeline()
        redis_pipeline.setex('sms_code_' + mobile, constants.SMS_CODE_EXPIRES, code)  # 设置短信验证码过期时间
        redis_pipeline.setex('sms_flag_' + mobile, constants.SMS_FLAG_EXPIRES, 1)  # 设置发送标志过期时间,不超过60s
        redis_pipeline.execute()  # 执行上述所有的redis管道命令

        """
        使用云通讯来发送短信验证码
        sendSMS.py文件中的类CCP的实例执行sendTemplateSMS()方法来执行发送
        """
        # CCP.sendTemplateSMS(mobile, code, constants.SMS_CODE_EXPIRES/60, 1)
        print(code)

        return Response('ok,ok')
