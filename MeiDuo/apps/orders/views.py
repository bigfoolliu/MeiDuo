from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer
from goods.models import SKU


class CartListView(APIView):
    """
    构造订单需要获取购物车中选中的商品
    因为不操作模型类，所以直接继承APIView
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        读取redis中的用户购物车的信息
        :param request:
        :return:
        """
        redis_cli = get_redis_connection('cart')
        key_cart = 'cart_%d' % request.user.id
        key_selected = 'cart_selected_%d' % request.user.id

        # 读取hash中改用户的商品编号和数量
        cart_dict = redis_cli.hgetall(key_cart)
        # 读取set中改用户的商品编号(表示选定的状态)
        cart_selected = redis_cli.smembers(key_selected)
        # 转换格式
        cart_dict2 = {}
        for sku_id, count in cart_dict.items():
            cart_dict2[int(sku_id)] = int(count)
        cart_selected2 = [int(sku_id) for sku_id in cart_selected]

        print('cart_dict2:', cart_dict2)  # TODO:

        # 查询商品对象
        skus = SKU.objects.filter(pk__in=cart_selected2)
        # 遍历商品增加数量属性
        for sku in skus:
            sku.count = cart_dict2[sku.id]
            sku.selected = True

        # 序列化输出
        serializer = CartSerializer(skus, many=True)

        return Response({
            'freight': 10,  # 运费
            'skus': serializer.data
        })
