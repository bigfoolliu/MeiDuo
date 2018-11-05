#!-*-coding:utf-8-*-
# !@Date: 18-11-5 下午2:48
# !@Author: Liu Rui
# !@github: bigfoolliu
from django_redis import get_redis_connection

import myjson


def merge_cookie_to_redis(request, user_id, response):
    """
    将cookie中的购物车信息合并到登录用户的redis中
    供视图中调用,这里的合并是将cookie中的信息覆盖掉redis中的数据
    :param request:　获取携带的cookie
    :param user_id: 当前登录的用户
    :param response: 使用完成后删除cookie中的购物车信息
    :return:
    """
    # 读取cookie中的信息
    cart_str = request.COOKIES.get('cart')
    if cart_str is None:
        return response

    cart_dict = myjson.loads(cart_str)

    # 遍历字典中的信息将其写入到redis中
    redis_cli = get_redis_connection('cart')
    key_cart = 'cart_%d' % user_id
    key_selected = 'cart_selected_%d' % user_id
    """
    获取redis的管道，因为之后要对redis数据库进行多步的操作
    可以将不同的操作放入管道一起执行
    """
    redis_pipeline = redis_cli.pipline()
    for sku_id, sku_dict in cart_dict.items():
        # hash中存储商品编号以及数量
        redis_pipeline.hset(key_cart, sku_id, sku_dict['count'])
        # set中存储商品选中的状态
        if sku_dict['selected']:
            redis_pipeline.sadd(key_selected, sku_id)
        else:
            redis_pipeline.srem(key_selected, sku_id)
    # 执行管道中的命令
    redis_pipeline.execute()

    # 将cookie中的数据删除
    response.set_cookie('cart', '', max_age=0)  # 删除数据的重点是将其过期时间设置为0

