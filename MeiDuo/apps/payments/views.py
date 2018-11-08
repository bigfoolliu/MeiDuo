from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay import AliPay

from orders.models import OrderInfo
from payments.models import Payment


class AliPayURLView(APIView):
    """
    生成支付的url后端接口
    """

    def get(self, request, order_id):
        """
        根据查询字符串中的信息返回支付宝支付url
        :param request:
        :param order_id:
        :return:
        """
        # 根据订单号来查询订单对象
        try:
            order = OrderInfo.objects.get(pk=order_id)
        except:
            raise Exception('订单编号无效')

        # 创建一个alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=settings.ALIPAY_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG,
        )

        # 调用方法生成支付url的参数
        order_string = alipay.api_alipay_trade_page_pay(
            subject=settings.ALIPAY_SUBJECT,
            out_trade_no=order_id,  # 订单编号
            total_amount=str(order.total_amount),  # 支付总金额,原始类型为Decimal(),不支持序列化，需要强转成str
            return_url=settings.ALIPAY_RETURN_URL,
        )

        # 拼接支付的url
        alipay_url = settings.ALIPAY_GATE + order_string

        return Response({'alipay_url': alipay_url})


class OrderStatusView(APIView):
    """
    更改订单状态的后端接口
    """

    def put(self, request):
        """
        修改接口,前端接口写好的在支付宝回调成功之后会向该接口发送put请求
        :param request:
        :return:
        """
        # 接收支付宝传回的参数
        alipay_dict = request.query_params.dict()
        print(alipay_dict)  # TODO:
        """
        {
            'charset': 'utf-8',
            'out_trade_no': '20181108095831000000002',
            'method': 'alipay.trade.page.pay.return',
            'total_amount': '3388.00',
            'sign': 'olaFS6DzzImUox3hPOa1CIKPle6/
                3TX7fsdTBJpIorS0fC7tMB5ASio34Z/
                GWvodSZvPx3vWc39+tcnQZJd0aZmuRFdK6w7IWb/
                oIjUm9K94RnHe51Z8n8p+JLnzHuCaXglunUm0gbwwOdyUcx3U7ajC3qGsQYSWdLyVCkdlzL+E3zovenOeuzezcfTsF+ca8G82yfoCGw/
                vZ/HPqMWV3ZK7/HPL4LhyVzu4xHocSb0wMn+QfUNMPjs8ke4ObGB/
                1MOHZ7I7UMWWcPErHaVgMDOzegEb+2oxzxqs+VAGsRZ63w0wsMc6AFQ+wdAYofaN1UB6jetS9HNV4uE8O5qGSw==',
            'trade_no': '2018110822001490630501366789',
            'auth_app_id': '2016092000553612',
            'version': '1.0',
            'app_id': '2016092000553612',
            'sign_type': 'RSA2',
            'seller_id': '2088102176447161',
            'timestamp': '2018-11-08 09:59:30'
        }
        """

        # 验证是否支付成功
        signature = alipay_dict.pop('sign')  # 删除签名，不参与验证，alipay官档规定
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=settings.ALIPAY_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG,
        )
        success = alipay.verify(alipay_dict, signature)  # 验证
        if success:
            # 支付成功
            order_id = alipay_dict['out_trade_no']
            # 获取订单
            try:
                order = OrderInfo.objects.get(pk=order_id)
            except:
                raise Exception('订单编号无效')
            else:
                # 更改订单状态
                order.status = 2  # 将订单的默认未付款状态改为未发货状态
                order.save()

            # 创建订单支付对象
            trade_no = alipay_dict.get('trade_no')  # alipay创建的流水号
            Payment.objects.create(
                order_id=order_id,
                trade_no=trade_no
            )
            # 返回响应
            return Response({'trade_no': trade_no})
        else:
            raise Exception('支付失败')

