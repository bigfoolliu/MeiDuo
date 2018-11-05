import logging
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from MeiDuo.utils import myjson
from carts import constants
from carts.serializers import CartAddSerializer, CartSerializer, CartDeleteSerializer, CartSelectSerializer
from goods.models import SKU

logger = logging.getLogger('django')


class CartView(APIView):
    """
    添加商品至购物车的视图接口
    """

    def perform_authentication(self, request):
        """
        继承自APIView,会自动对用户进行认证
        重写该方法使在执行该视图函数之前不进行身份检查
        :param request:
        :return:
        """
        pass

    def post(self, request):
        """
        添加至购物车
        :param request:
        :return:
        """
        # 判断用户是否登录
        try:
            user = request.user
        except Exception as e:
            logging.info(e)
            user = None

        # 接收请求数据进行验证
        serializer = CartAddSerializer(data=request.data)
        # 序列化器进行验证不过则直接报异常,且异常会在配置中的异常处理类来处理
        serializer.is_valid(raise_exception=True)
        # 获取验证通过的数据
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']

        # 构造响应对象
        response = Response(serializer.validated_data)

        """
        用户未登录则使用cookie存储用户加入购物车的信息
        cookie的原始信息如下,但是后面的字典是经过base64加密的
        cart: {
            'sku_id': {
                'count': xxx,
                'selected': xxx
            }
        }
        """
        if user is None:
            cart_str = request.COOKIES.get('cart')  # 获取cookie

            print('cart_str:', cart_str)  # TODO:

            if cart_str is None:
                cart_dict = {}
            else:
                cart_dict = myjson.loads(cart_str)
            # 取出原始数量
            if sku_id in cart_dict:
                count_cart = cart_dict[sku_id]['count']
            else:
                count_cart = 0
            # 修改购物车中相关数据(包括商品的数量以及商品是否勾选状态)
            cart_dict[sku_id] = {
                'count': count + count_cart,
                'selected': True
            }
            # 将信息写到cookie中
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            """
            如果用户登录,则使用redis进行存储
            """
            # 连接redis并构造键
            redis_cli = get_redis_connection('cart')
            key = 'cart_%d' % request.user.id
            key_select = 'cart_select_%d' % request.user.id
            # 将商品编号及数量存入hash中
            redis_cli.hset(key, sku_id, count)
            # 将商品编号存入set中表示选中该商品
            redis_cli.sadd(key_select, sku_id)

        # 返回响应数据
        return response

    def get(self, request):
        """
        查找购物车中商品信息
        :param request:
        :return:
        """
        # 判断用户是否登录
        try:
            user = request.user
        except Exception as e:
            logging.info(e)
            user = None

        # 用户未登录读取cookie
        if user is None:
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            # 根据商品编号查询对象并添加数量和选中属性
            skus = []
            print('cart_dict:', cart_dict, type(cart_dict))  # TODO:
            for key, value in cart_dict.items():
                sku = SKU.objects.get(pk=key)
                sku.count = value['count']
                sku.selected = value['selected']
                skus.append(sku)
        else:
            # 用户登录读取redis
            # 连接redis并构造键
            redis_cli = get_redis_connection('cart')
            key = 'cart_%d' % request.user.id
            key_select = 'cart_select_%d' % request.user.id
            # 从hash中读取该用户加入购物车的所有的商品编号
            sku_ids = redis_cli.hkeys(key)
            # 读取选中的商品编号
            sku_ids_selected = redis_cli.smembers(key_select)
            sku_ids_selected = [int(sku_id) for sku_id in sku_ids_selected]  # 从redis中取出的数据为字节需转换
            # 查询商品
            skus = SKU.objects.filter(pk__in=sku_ids)
            # 遍历商品,增加数量并选中属性
            for sku in skus:
                sku.count = redis_cli.hget(key, sku.id)
                sku.selected = sku.id in sku_ids_selected
        # 序列化输出
        serializer = CartSerializer(skus, many=True)

        # print(serializer.data)  # TODO: 测试

        return Response(serializer.data)

    def put(self, request):
        """
        修改购物车商品
        :param request:
        :return:
        """
        # 判断用户是否登录
        try:
            user = request.user
        except Exception as e:
            logging.info(e)
            user = None

        # 接收数据并验证
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取验证之后的数据
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        # 构造相应数据
        response = Response(serializer.validated_data)

        if user is None:
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            redis_cli = get_redis_connection('cart')
            key = 'cart_%d' % request.user.id
            key_select = 'cart_select_%d' % request.user.id
            # 修改数量
            redis_cli.hset(key, sku_id, count)
            # 修改选中状态
            if selected:
                redis_cli.sadd(key_select, sku_id)
            else:
                redis_cli.srem(key_select, sku_id)
        # 返回响应
        return response

    def delete(self, request):
        """
        删除购物车中的商品
        :param request:
        :return:
        """
        try:
            user = request.user
        except Exception as e:
            logger.info(e)
            user = None

        serializer = CartDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data['sku_id']

        response = Response(status=204)

        if user is None:
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            # 删除
            if sku_id in cart_dict:
                del cart_dict[sku_id]
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            redis_cli = get_redis_connection('cart')
            key = 'cart_%d' % request.user.id
            key_select = 'cart_selected_%d' % request.user.id
            redis_cli.hdel(key, sku_id)
            redis_cli.srem(key_select, sku_id)

        return response


class CartSelectView(APIView):
    """
    购物车中选中或者取消选中商品，只需要传递一个参数selected
    """

    def perform_authentication(self, request):
        """
        取消APIView的用户验证
        :param request:
        :return:
        """
        pass

    def put(self, request):
        """
        属于修改操作
        :param request:
        :return:
        """
        try:
            user = request.user
        except Exception as e:
            logger.info(e)
            user = None

        serializer = CartSelectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected = serializer.validated_data['selected']

        response = Response({'message': 'OK'})

        if user is None:
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            # 遍历所有的键逐个修改selected的值
            for key in cart_dict.keys():
                cart_dict[key]['selected'] = selected
        else:
            redis_cli = get_redis_connection('cart')
            key = 'cart_%d' % request.user.id
            key_select = 'cart_select_%d' % request.user.id
            # 获取所有的商品编号
            sku_ids = request.hkeys(key)
            if selected:
                redis_cli.sadd(key_select, *sku_ids)
            else:
                redis_cli.srem(key_select, *sku_ids)

        return response
