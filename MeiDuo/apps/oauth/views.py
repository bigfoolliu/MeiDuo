import logging

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth import constants
from oauth.models import QQUser
from oauth.qq_sdk import OAuthQQ


from oauth.serializes import QQBindSerializer
from MeiDuo.utils import tjws
from MeiDuo.utils.jwt_token import generate

logger = logging.getLogger('django')


# 127.0.0.1:8000/oauth/qq/authorization/?next=
class QQurlView(APIView):
    """
    获取qq登录的url(即带有输入qq账号,密码以及二维码登录的页面)
    """

    def get(self, request):
        """
        GET请求
        :param request:
        :return:
        """
        # 接收登录后的地址(请求字符串中携带的参数)
        state = request.query_params.get('next')
        # 创建工具类对象
        oauthqq = OAuthQQ(state=state)
        # 获取授权地址
        url = oauthqq.get_qq_login_url()
        # 响应
        return Response({
            'login_url': url
        })


# 127.0.0.1:8000/oauth/qq/user/?code=
class QQLoginView(APIView):
    """
    填写qq账号和密码之后的回调
    """

    def get(self, request):
        """
        GET请求
        :param request:
        :return:
        """
        # 获取code
        code = request.query_params.get('code')

        # 根据code获取token
        oauthqq = OAuthQQ()
        token = oauthqq.get_access_token(code)

        # 根据token获取openid
        openid = oauthqq.get_openid(token)

        # 查询openid是否存在,即之前是否已经用qq号绑定了一个注册账号
        try:
            qquser = QQUser.objects.get(openid=openid)
        except Exception as e:
            logger.error(e)
            # 如果不存在,则通知客户端的转到绑定页面
            # 将openid加密进行输出
            data = tjws.dumps({'openid': openid}, constants.BIND_TOKEN_EXPIRES)
            # 响应
            return Response({
                'access_token': data
            })
        else:
            # 如果存在则进行状态保持,登录成功
            return Response({
                'user_id': qquser.user.id,
                'username': qquser.user.username,
                'token': generate(qquser.user)  # 生成token值
            })

    def post(self, request):
        """
        绑定之前的账户时接口
        :param request:
        :return:
        """
        # 接收
        serializer = QQBindSerializer(data=request.data)
        # 验证数据
        if not serializer.is_valid():
            return Response({'message': serializer.errors})
        # 绑定: 在qquser表中创建一条数据
        qquser = serializer.save()
        # 响应
        return Response({
            'user_id': qquser.user.id,
            'username': qquser.user.username,
            'token': generate(qquser.user)
        })

