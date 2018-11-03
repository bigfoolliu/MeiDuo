#!-*-coding:utf-8-*-
# !@Date: 18-11-2 下午10:45
# !@Author: Liu Rui
# !@github: bigfoolliu
from collections import OrderedDict

from goods.models import GoodsChannel


def get_goods_category():
    """
    获取商品的目录
    一个组（频道）包含几个一级分类，一个一级分类包含几个二级分类，一个二级分类包含几个三级分类
    :return:
    """
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')

    # 遍历频道，向不同级别的分类中添加数据
    for channel in channels:
        if channel.group_id not in categories:
            categories[channel.group_id] = {'channels': [], 'sub_cats': []}
        # 添加一级分类
        categories[channel.group_id]['channels'].append({
            'id': channel.id,
            'name': channel.category.name,
            'url': channel.url
        })
        # 添加二级分类
        sub_cats = channel.category.goodscategory_set.all()
        # 添加三级分类
        for sub in sub_cats:
            sub.sub_cats = sub.goodscategory_set.all()
            categories[channel.group_id]['sub_cats'].append(sub)

    # print(categories)
    return categories
