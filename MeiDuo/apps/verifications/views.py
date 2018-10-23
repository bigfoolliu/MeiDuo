from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class SMSCodeView(APIView):
    """
    短信验证视图类
    """
    def get(self, request, mobile):
        """
        限制最少每隔60s才向一个手机号发送短信验证码
        :param request:
        :param mobile:
        :return:
        """
        return Response('ok,ok')
